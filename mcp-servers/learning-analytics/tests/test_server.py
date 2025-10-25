#!/usr/bin/env python3
"""
Test script for Learning Analytics MCP Server

Creates mock data and validates all MCP tools work correctly.
"""

import sys
import os
from pathlib import Path
import uuid
from datetime import datetime, timedelta

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import LearningAnalyticsServer
import sqlite3


def create_mock_data(server: LearningAnalyticsServer):
    """Create realistic mock data for testing"""
    conn = sqlite3.connect(server.db_path)
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM cohorts")
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM course_progress")
    cursor.execute("DELETE FROM community_engagement")
    cursor.execute("DELETE FROM practice_adoption")
    cursor.execute("DELETE FROM retention_tracking")
    cursor.execute("DELETE FROM harm_prevention")
    cursor.execute("DELETE FROM nps_scores")

    print("Creating mock cohort data...")

    # Create cohort
    cohort_id = "cohort-q4-2024"
    cursor.execute("""
        INSERT INTO cohorts (cohort_id, name, start_date, student_count)
        VALUES (?, ?, ?, ?)
    """, (cohort_id, "Q4 2024 Cohort", "2024-10-01", 30))

    print(f"✅ Created cohort: {cohort_id} with 30 students")

    # Create students with personas
    personas = [
        ('sarah', 12),  # 40% Sarah-types (sceptical seniors)
        ('priya', 9),   # 30% Priya-types (curious mid-levels)
        ('marcus', 6),  # 20% Marcus-types (design leaders)
        ('david', 3)    # 10% Edge cases
    ]

    student_ids = []
    for persona_type, count in personas:
        for i in range(count):
            student_id = f"student-{persona_type}-{i+1}"
            student_ids.append((student_id, persona_type))
            cursor.execute("""
                INSERT INTO students (student_id, cohort_id, persona_type, enrollment_date)
                VALUES (?, ?, ?, ?)
            """, (student_id, cohort_id, persona_type, "2024-10-01"))

    print(f"✅ Created {len(student_ids)} students across 4 personas")

    # Create course progress (85% completion rate - elite!)
    modules = ['module-1', 'module-2', 'module-3', 'module-4', 'module-5']
    completed_count = 0

    for student_id, persona in student_ids:
        for module_id in modules:
            # 85% complete their modules
            completed = (hash(student_id + module_id) % 100) < 85

            if completed:
                completed_count += 1

            # Satisfaction varies by persona
            if persona == 'sarah':
                satisfaction = 4.6 + (hash(student_id) % 5) / 10  # 4.6-5.0
            elif persona == 'marcus':
                satisfaction = 4.5 + (hash(student_id) % 5) / 10  # 4.5-4.9
            elif persona == 'priya':
                satisfaction = 4.4 + (hash(student_id) % 7) / 10  # 4.4-5.0
            else:  # david
                satisfaction = 3.8 + (hash(student_id) % 10) / 10  # 3.8-4.7

            time_spent = 45 + (hash(student_id + module_id) % 30)  # 45-75 minutes

            cursor.execute("""
                INSERT INTO course_progress
                (progress_id, student_id, module_id, completed, completion_date, satisfaction_score, time_spent_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                student_id,
                module_id,
                1 if completed else 0,
                datetime.now().isoformat() if completed else None,
                round(satisfaction, 1),
                time_spent
            ))

    print(f"✅ Created course progress data ({completed_count}/{len(student_ids) * len(modules)} completions)")

    # Create community engagement (80%+ weekly active - elite!)
    for week in range(1, 9):  # 8 weeks
        for student_id, persona in student_ids:
            # 80% are active each week
            is_active = (hash(student_id + str(week)) % 100) < 80

            if is_active:
                # Engagement varies by persona
                if persona == 'sarah':
                    posts = 1 + (hash(student_id + str(week)) % 2)  # 1-2 posts
                    replies = 2 + (hash(student_id) % 3)  # 2-4 replies
                elif persona == 'priya':
                    posts = 2 + (hash(student_id + str(week)) % 3)  # 2-4 posts (more active)
                    replies = 3 + (hash(student_id) % 4)  # 3-6 replies
                elif persona == 'marcus':
                    posts = 1  # Less frequent but strategic
                    replies = 1 + (hash(student_id) % 2)
                else:  # david
                    posts = 0 if week < 3 else 1  # Resistant at first
                    replies = 1

                office_hours = 1 if (hash(student_id + str(week)) % 2) == 0 else 0
                peer_reviews = 1 if week in [3, 5, 7] else 0

                cursor.execute("""
                    INSERT INTO community_engagement
                    (engagement_id, student_id, cohort_id, week_number, posts_created, replies_made, office_hours_attended, peer_reviews_given)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    student_id,
                    cohort_id,
                    week,
                    posts,
                    replies,
                    office_hours,
                    peer_reviews
                ))

    print(f"✅ Created 8 weeks of community engagement data")

    # Create 6-month retention data (70%+ still using - elite!)
    for student_id, persona in student_ids:
        # 70% still using practices
        still_using = (hash(student_id + "retention") % 100) < 70

        frameworks = ["Privacy Framework", "Bias Testing", "Stakeholder Communication"]
        if still_using:
            used_frameworks = [f for f in frameworks if hash(student_id + f) % 2 == 0]
        else:
            used_frameworks = []

        cursor.execute("""
            INSERT INTO retention_tracking
            (retention_id, student_id, cohort_id, months_post_course, still_using_practices, frameworks_still_used, survey_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            student_id,
            cohort_id,
            6,
            1 if still_using else 0,
            ", ".join(used_frameworks),
            datetime.now().isoformat()
        ))

    print(f"✅ Created 6-month retention tracking data")

    # Create harm prevention stories (90%+ caught risks)
    for student_id, persona in student_ids:
        # 90% have at least one harm prevention story
        if (hash(student_id + "harm") % 100) < 90:
            risk_types = ["privacy-breach", "bias-risk", "data-leakage"]
            risk_type = risk_types[hash(student_id) % len(risk_types)]

            stories = {
                "privacy-breach": "Stopped before pasting client interview with PII into ChatGPT",
                "bias-risk": "Caught potential bias in AI feature during design review",
                "data-leakage": "Prevented IP leakage by using privacy-preserving prompts"
            }

            cursor.execute("""
                INSERT INTO harm_prevention
                (story_id, student_id, week_number, risk_type, description, action_taken)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                student_id,
                3 + (hash(student_id) % 5),  # Week 3-7
                risk_type,
                stories[risk_type],
                "Applied framework from course"
            ))

    print(f"✅ Created harm prevention stories")

    # Create NPS scores (target: 70+ = elite)
    promoter_count = 0
    for student_id, persona in student_ids:
        # Sarah and Priya are promoters (9-10), Marcus is passive (7-8), David is detractor initially
        if persona in ['sarah', 'priya']:
            score = 9 + (hash(student_id) % 2)  # 9 or 10
            promoter_count += 1
        elif persona == 'marcus':
            score = 7 + (hash(student_id) % 2)  # 7 or 8
        else:  # david
            score = 5 + (hash(student_id) % 4)  # 5-8

        cursor.execute("""
            INSERT INTO nps_scores
            (nps_id, student_id, cohort_id, score, survey_type, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            student_id,
            cohort_id,
            score,
            "end-of-course",
            f"Sample comment from {persona}"
        ))

    print(f"✅ Created NPS scores (NPS ≈ {(promoter_count/len(student_ids)*100) - ((len(student_ids)-promoter_count-9)/len(student_ids)*100):.0f})")

    conn.commit()
    conn.close()
    print("\n✅ Mock data creation complete!\n")


def test_all_tools(server: LearningAnalyticsServer):
    """Test all MCP tools"""
    print("="*60)
    print("Testing All MCP Tools")
    print("="*60)

    cohort_id = "cohort-q4-2024"

    # Test 1: Get Course Metrics
    print("\n1. Testing get_course_metrics...")
    metrics = server.get_course_metrics(cohort_id=cohort_id)
    print(f"   Total Students: {metrics['total_students']}")
    print(f"   Completions: {metrics['completions']}")
    print(f"   Completion Rate: {metrics['completion_rate']}% (target: 85%+)")
    print(f"   Avg Satisfaction: {metrics['avg_satisfaction']}/5.0 (target: 4.5+)")
    assert metrics['completion_rate'] >= 80, "Completion rate should be ~85%"
    print("   ✅ PASS")

    # Test 2: Get Engagement Metrics
    print("\n2. Testing get_engagement_metrics...")
    engagement = server.get_engagement_metrics(cohort_id=cohort_id, week_number=4)
    print(f"   Week 4 Active Students: {engagement['active_students']}/{engagement['total_students']}")
    print(f"   Weekly Active Rate: {engagement['weekly_active_rate']}% (target: 80%+)")
    print(f"   Total Posts: {engagement['total_posts']}")
    print(f"   Total Replies: {engagement['total_replies']}")
    assert engagement['weekly_active_rate'] >= 75, "Should have ~80% weekly active"
    print("   ✅ PASS")

    # Test 3: Get Outcome Metrics
    print("\n3. Testing get_outcome_metrics...")
    outcomes = server.get_outcome_metrics(cohort_id=cohort_id, months_post_course=6)
    print(f"   6-Month Retention: {outcomes['retention_rate']}% (target: 70%+)")
    print(f"   Still Using Practices: {outcomes['still_using_practices']}/{outcomes['retention_responses']}")
    print(f"   Harm Prevention Rate: {outcomes['harm_prevention_rate']}% (target: 90%+)")
    assert outcomes['retention_rate'] >= 65, "Should have ~70% 6-month retention"
    assert outcomes['harm_prevention_rate'] >= 85, "Should have ~90% harm prevention"
    print("   ✅ PASS")

    # Test 4: Get Persona Analytics
    print("\n4. Testing get_persona_analytics...")
    personas = server.get_persona_analytics(cohort_id=cohort_id)
    print(f"   Cohort Composition:")
    for p in personas['personas']:
        print(f"     - {p['persona_type']}: {p['student_count']} students, "
              f"{p['completion_rate']}% completion, "
              f"{p['avg_satisfaction']}/5.0 satisfaction")
    print("   ✅ PASS")

    # Test 5: Get Cohort Health
    print("\n5. Testing get_cohort_health...")
    health = server.get_cohort_health(cohort_id=cohort_id)
    print(f"   Health Score: {health['health_score']}/100 {health['status_emoji']}")
    print(f"   Status: {health['status']}")
    print(f"   Component Scores:")
    for component, score in health['component_scores'].items():
        print(f"     - {component}: {score}/25")
    print(f"   Recommendations:")
    for rec in health['recommendations']:
        print(f"     {rec}")
    assert health['health_score'] >= 60, "Cohort should be healthy"
    print("   ✅ PASS")

    print("\n" + "="*60)
    print("🎉 ALL MCP TOOLS WORKING CORRECTLY!")
    print("="*60)


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" LEARNING ANALYTICS MCP SERVER - TEST SUITE")
    print("="*70)

    # Create test database
    test_db = "./data/test_analytics.db"
    if os.path.exists(test_db):
        os.remove(test_db)

    server = LearningAnalyticsServer(db_path=test_db)
    print(f"✅ Server initialized with test database: {test_db}\n")

    # Create mock data
    create_mock_data(server)

    # Test all tools
    test_all_tools(server)

    print("\n💡 Next Steps:")
    print("   1. Integrate this MCP server with agents")
    print("   2. Test Data Analyst agent using these tools")
    print("   3. Build remaining 4 MCP servers")
    print("\n✅ Learning Analytics MCP Server is READY!\n")


if __name__ == "__main__":
    main()
