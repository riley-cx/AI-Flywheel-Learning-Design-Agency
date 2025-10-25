#!/usr/bin/env python3
"""
Learning Analytics MCP Server

MCP server that provides learning analytics data to AI agents.
Follows Anthropic's MCP specification for tool integration.

Key Tools Provided:
- get_course_metrics: Completion rates, satisfaction scores
- get_engagement_metrics: Community activity, practice adoption
- get_outcome_metrics: 6-month retention, harm prevention
- get_persona_analytics: Performance by student persona
- get_cohort_health: Overall cohort status
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path


class LearningAnalyticsServer:
    """
    MCP Server for Learning Analytics

    Provides AI agents with access to student performance,
    engagement, and outcome data for data-driven decision making.
    """

    def __init__(self, db_path: str = "./data/analytics.db"):
        """
        Initialize the Learning Analytics MCP Server

        Args:
            db_path: Path to SQLite database with analytics data
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database schema if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Cohorts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cohorts (
                cohort_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                student_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                cohort_id TEXT NOT NULL,
                persona_type TEXT,
                enrollment_date TEXT NOT NULL,
                FOREIGN KEY (cohort_id) REFERENCES cohorts(cohort_id)
            )
        """)

        # Course progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course_progress (
                progress_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                module_id TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                completion_date TEXT,
                satisfaction_score REAL,
                time_spent_minutes INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Community engagement table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS community_engagement (
                engagement_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                cohort_id TEXT NOT NULL,
                week_number INTEGER NOT NULL,
                posts_created INTEGER DEFAULT 0,
                replies_made INTEGER DEFAULT 0,
                office_hours_attended INTEGER DEFAULT 0,
                peer_reviews_given INTEGER DEFAULT 0,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Practice adoption table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS practice_adoption (
                adoption_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                framework_name TEXT NOT NULL,
                week_number INTEGER NOT NULL,
                self_reported BOOLEAN DEFAULT 0,
                evidence_shared BOOLEAN DEFAULT 0,
                peer_validated BOOLEAN DEFAULT 0,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Retention tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retention_tracking (
                retention_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                cohort_id TEXT NOT NULL,
                months_post_course INTEGER NOT NULL,
                still_using_practices BOOLEAN,
                frameworks_still_used TEXT,
                evidence_provided TEXT,
                survey_date TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Harm prevention stories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS harm_prevention (
                story_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                week_number INTEGER,
                risk_type TEXT,
                description TEXT,
                action_taken TEXT,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # NPS scores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nps_scores (
                nps_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                cohort_id TEXT NOT NULL,
                score INTEGER NOT NULL CHECK (score >= 0 AND score <= 10),
                survey_type TEXT NOT NULL,
                comment TEXT,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        conn.commit()
        conn.close()

    def get_course_metrics(
        self,
        cohort_id: Optional[str] = None,
        module_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get course performance metrics

        MCP Tool: get_course_metrics

        Args:
            cohort_id: Filter by specific cohort (optional)
            module_id: Filter by specific module (optional)

        Returns:
            Dictionary with completion rates, satisfaction scores, time metrics
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Build query with optional filters
        query = """
            SELECT
                COUNT(DISTINCT cp.student_id) as total_students,
                SUM(CASE WHEN cp.completed = 1 THEN 1 ELSE 0 END) as completions,
                ROUND(AVG(cp.satisfaction_score), 2) as avg_satisfaction,
                ROUND(AVG(cp.time_spent_minutes), 0) as avg_time_minutes
            FROM course_progress cp
            JOIN students s ON cp.student_id = s.student_id
            WHERE 1=1
        """

        params = []
        if cohort_id:
            query += " AND s.cohort_id = ?"
            params.append(cohort_id)
        if module_id:
            query += " AND cp.module_id = ?"
            params.append(module_id)

        cursor.execute(query, params)
        row = cursor.fetchone()

        total = row['total_students'] or 0
        completions = row['completions'] or 0

        result = {
            'total_students': total,
            'completions': completions,
            'completion_rate': round((completions / total * 100), 1) if total > 0 else 0,
            'avg_satisfaction': row['avg_satisfaction'] or 0,
            'avg_time_minutes': row['avg_time_minutes'] or 0,
            'filters_applied': {
                'cohort_id': cohort_id,
                'module_id': module_id
            }
        }

        conn.close()
        return result

    def get_engagement_metrics(
        self,
        cohort_id: str,
        week_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get community engagement metrics

        MCP Tool: get_engagement_metrics

        Args:
            cohort_id: Cohort to analyze
            week_number: Filter by specific week (optional)

        Returns:
            Dictionary with community activity metrics
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
            SELECT
                COUNT(DISTINCT student_id) as active_students,
                SUM(posts_created) as total_posts,
                SUM(replies_made) as total_replies,
                SUM(office_hours_attended) as total_office_hours,
                SUM(peer_reviews_given) as total_peer_reviews
            FROM community_engagement
            WHERE cohort_id = ?
        """

        params = [cohort_id]
        if week_number:
            query += " AND week_number = ?"
            params.append(week_number)

        cursor.execute(query, params)
        row = cursor.fetchone()

        # Get total students in cohort
        cursor.execute(
            "SELECT student_count FROM cohorts WHERE cohort_id = ?",
            (cohort_id,)
        )
        cohort_row = cursor.fetchone()
        total_students = cohort_row['student_count'] if cohort_row else 0

        active = row['active_students'] or 0

        result = {
            'cohort_id': cohort_id,
            'week_number': week_number,
            'total_students': total_students,
            'active_students': active,
            'weekly_active_rate': round((active / total_students * 100), 1) if total_students > 0 else 0,
            'total_posts': row['total_posts'] or 0,
            'total_replies': row['total_replies'] or 0,
            'total_office_hours': row['total_office_hours'] or 0,
            'total_peer_reviews': row['total_peer_reviews'] or 0,
            'avg_posts_per_student': round((row['total_posts'] or 0) / active, 1) if active > 0 else 0
        }

        conn.close()
        return result

    def get_outcome_metrics(
        self,
        cohort_id: str,
        months_post_course: int = 6
    ) -> Dict[str, Any]:
        """
        Get outcome metrics (6-month retention, harm prevention)

        MCP Tool: get_outcome_metrics

        Args:
            cohort_id: Cohort to analyze
            months_post_course: Number of months post-course (default: 6)

        Returns:
            Dictionary with outcome metrics
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get retention data
        cursor.execute("""
            SELECT
                COUNT(*) as total_responses,
                SUM(CASE WHEN still_using_practices = 1 THEN 1 ELSE 0 END) as still_using
            FROM retention_tracking
            WHERE cohort_id = ? AND months_post_course = ?
        """, (cohort_id, months_post_course))

        retention_row = cursor.fetchone()
        total_responses = retention_row['total_responses'] or 0
        still_using = retention_row['still_using'] or 0

        # Get harm prevention stories
        cursor.execute("""
            SELECT COUNT(DISTINCT hp.student_id) as students_with_stories
            FROM harm_prevention hp
            JOIN students s ON hp.student_id = s.student_id
            WHERE s.cohort_id = ?
        """, (cohort_id,))

        harm_row = cursor.fetchone()

        # Get cohort size
        cursor.execute(
            "SELECT student_count FROM cohorts WHERE cohort_id = ?",
            (cohort_id,)
        )
        cohort_row = cursor.fetchone()
        total_students = cohort_row['student_count'] if cohort_row else 0

        result = {
            'cohort_id': cohort_id,
            'months_post_course': months_post_course,
            'total_students': total_students,
            'retention_responses': total_responses,
            'still_using_practices': still_using,
            'retention_rate': round((still_using / total_responses * 100), 1) if total_responses > 0 else 0,
            'harm_prevention_stories': harm_row['students_with_stories'] or 0,
            'harm_prevention_rate': round(
                ((harm_row['students_with_stories'] or 0) / total_students * 100), 1
            ) if total_students > 0 else 0
        }

        conn.close()
        return result

    def get_persona_analytics(
        self,
        cohort_id: str,
        persona_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get analytics by student persona

        MCP Tool: get_persona_analytics

        Args:
            cohort_id: Cohort to analyze
            persona_type: Filter by persona (sarah, marcus, priya) - optional

        Returns:
            Dictionary with persona-specific performance data
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
            SELECT
                s.persona_type,
                COUNT(DISTINCT s.student_id) as student_count,
                ROUND(AVG(CASE WHEN cp.completed = 1 THEN 1.0 ELSE 0.0 END) * 100, 1) as completion_rate,
                ROUND(AVG(cp.satisfaction_score), 2) as avg_satisfaction
            FROM students s
            LEFT JOIN course_progress cp ON s.student_id = cp.student_id
            WHERE s.cohort_id = ?
        """

        params = [cohort_id]
        if persona_type:
            query += " AND s.persona_type = ?"
            params.append(persona_type)

        query += " GROUP BY s.persona_type"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        personas = []
        for row in rows:
            personas.append({
                'persona_type': row['persona_type'],
                'student_count': row['student_count'],
                'completion_rate': row['completion_rate'] or 0,
                'avg_satisfaction': row['avg_satisfaction'] or 0
            })

        result = {
            'cohort_id': cohort_id,
            'filter_persona': persona_type,
            'personas': personas
        }

        conn.close()
        return result

    def get_cohort_health(self, cohort_id: str) -> Dict[str, Any]:
        """
        Get overall cohort health score

        MCP Tool: get_cohort_health

        Combines multiple metrics into health assessment:
        - Completion rate (target: 85%+)
        - Community engagement (target: 80%+ weekly active)
        - Satisfaction (target: 4.5/5.0)
        - Practice adoption (target: 75%+)

        Args:
            cohort_id: Cohort to assess

        Returns:
            Dictionary with health score and component metrics
        """
        conn = sqlite3.connect(self.db_path)

        # Get course metrics
        course_metrics = self.get_course_metrics(cohort_id=cohort_id)

        # Get latest week engagement
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(week_number) as latest_week
            FROM community_engagement
            WHERE cohort_id = ?
        """, (cohort_id,))
        latest_week = cursor.fetchone()[0]

        engagement_metrics = self.get_engagement_metrics(
            cohort_id=cohort_id,
            week_number=latest_week
        ) if latest_week else {'weekly_active_rate': 0}

        # Calculate health score (0-100)
        completion_score = min(course_metrics['completion_rate'] / 85 * 25, 25)
        engagement_score = min(engagement_metrics['weekly_active_rate'] / 80 * 25, 25)
        satisfaction_score = min((course_metrics['avg_satisfaction'] / 4.5) * 25, 25)

        # Practice adoption (simplified for now)
        practice_score = 15  # Placeholder

        health_score = round(
            completion_score + engagement_score + satisfaction_score + practice_score,
            1
        )

        # Determine status
        if health_score >= 80:
            status = "ELITE"
            status_emoji = "🏆"
        elif health_score >= 60:
            status = "HEALTHY"
            status_emoji = "✅"
        elif health_score >= 40:
            status = "NEEDS_ATTENTION"
            status_emoji = "⚠️"
        else:
            status = "AT_RISK"
            status_emoji = "❌"

        result = {
            'cohort_id': cohort_id,
            'health_score': health_score,
            'status': status,
            'status_emoji': status_emoji,
            'component_scores': {
                'completion': round(completion_score, 1),
                'engagement': round(engagement_score, 1),
                'satisfaction': round(satisfaction_score, 1),
                'practice_adoption': practice_score
            },
            'metrics': {
                'completion_rate': course_metrics['completion_rate'],
                'weekly_active_rate': engagement_metrics['weekly_active_rate'],
                'avg_satisfaction': course_metrics['avg_satisfaction']
            },
            'recommendations': self._get_health_recommendations(
                course_metrics,
                engagement_metrics
            )
        }

        conn.close()
        return result

    def _get_health_recommendations(
        self,
        course_metrics: Dict,
        engagement_metrics: Dict
    ) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []

        if course_metrics['completion_rate'] < 75:
            recommendations.append(
                "⚠️ Completion rate below target - investigate module difficulty or engagement"
            )

        if engagement_metrics['weekly_active_rate'] < 70:
            recommendations.append(
                "⚠️ Low community engagement - boost Slack activity and office hours attendance"
            )

        if course_metrics['avg_satisfaction'] < 4.0:
            recommendations.append(
                "⚠️ Satisfaction below target - review student feedback and module quality"
            )

        if not recommendations:
            recommendations.append("✅ All metrics healthy - maintain current approach")

        return recommendations


# MCP Server Tool Definitions (for integration with agents)
MCP_TOOLS = [
    {
        "name": "get_course_metrics",
        "description": "Get course completion rates, satisfaction scores, and time metrics",
        "input_schema": {
            "type": "object",
            "properties": {
                "cohort_id": {
                    "type": "string",
                    "description": "Filter by specific cohort ID (optional)"
                },
                "module_id": {
                    "type": "string",
                    "description": "Filter by specific module ID (optional)"
                }
            }
        }
    },
    {
        "name": "get_engagement_metrics",
        "description": "Get community engagement metrics (posts, replies, attendance)",
        "input_schema": {
            "type": "object",
            "properties": {
                "cohort_id": {
                    "type": "string",
                    "description": "Cohort ID to analyze"
                },
                "week_number": {
                    "type": "integer",
                    "description": "Filter by specific week number (optional)"
                }
            },
            "required": ["cohort_id"]
        }
    },
    {
        "name": "get_outcome_metrics",
        "description": "Get outcome metrics (6-month retention, harm prevention stories)",
        "input_schema": {
            "type": "object",
            "properties": {
                "cohort_id": {
                    "type": "string",
                    "description": "Cohort ID to analyze"
                },
                "months_post_course": {
                    "type": "integer",
                    "description": "Months after course completion (default: 6)"
                }
            },
            "required": ["cohort_id"]
        }
    },
    {
        "name": "get_persona_analytics",
        "description": "Get performance analytics by student persona (sarah, marcus, priya)",
        "input_schema": {
            "type": "object",
            "properties": {
                "cohort_id": {
                    "type": "string",
                    "description": "Cohort ID to analyze"
                },
                "persona_type": {
                    "type": "string",
                    "description": "Filter by persona: sarah, marcus, or priya (optional)"
                }
            },
            "required": ["cohort_id"]
        }
    },
    {
        "name": "get_cohort_health",
        "description": "Get overall cohort health score and recommendations",
        "input_schema": {
            "type": "object",
            "properties": {
                "cohort_id": {
                    "type": "string",
                    "description": "Cohort ID to assess"
                }
            },
            "required": ["cohort_id"]
        }
    }
]


if __name__ == "__main__":
    # Example usage
    server = LearningAnalyticsServer()
    print("Learning Analytics MCP Server initialized")
    print(f"Available tools: {[tool['name'] for tool in MCP_TOOLS]}")
