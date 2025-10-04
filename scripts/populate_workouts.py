#!/usr/bin/env python3
"""
Script to populate workout of the day examples
"""
import sys
import os
from datetime import date, timedelta
import json

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import WorkoutOfTheDay, Base

# Create tables
Base.metadata.create_all(bind=engine)

def create_sample_workouts():
    """Create sample workouts for the week"""
    db = SessionLocal()
    
    try:
        # Delete existing workouts
        db.query(WorkoutOfTheDay).delete()
        
        # Sample workouts
        workouts = [
            {
                "title": "Full Body HIIT Blast",
                "description": "High-intensity interval training targeting all major muscle groups. Perfect for burning calories and building strength.",
                "category": "hiit",
                "difficulty_level": "intermediate",
                "estimated_duration": 30,
                "main_exercises": [
                    {
                        "name": "Jumping Jacks",
                        "duration": "45 seconds",
                        "rest": "15 seconds",
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Burpees",
                        "duration": "30 seconds",
                        "rest": "30 seconds",
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Mountain Climbers",
                        "duration": "45 seconds",
                        "rest": "15 seconds",
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Push-ups",
                        "duration": None,
                        "rest": "30 seconds",
                        "reps": "10-15",
                        "sets": 3
                    },
                    {
                        "name": "Squat Jumps",
                        "duration": "30 seconds",
                        "rest": "30 seconds",
                        "reps": None,
                        "sets": 3
                    }
                ],
                "equipment_needed": ["none"],
                "calories_estimate": 350,
                "motivation_tip": "Perform each exercise for the specified duration with minimal rest between exercises. Complete 3 rounds with 2-minute rest between rounds.",
                "form_tips": ["Keep proper form even when tired", "Modify exercises if needed", "Stay hydrated"],
                "video_url": "https://example.com/hiit-workout",
                "thumbnail_url": "https://example.com/hiit-image.jpg",
                "featured": True,
                "date": date.today()
            },
            {
                "title": "Morning Yoga Flow",
                "description": "Gentle yoga sequence to start your day with energy and mindfulness. Focus on flexibility and breathing.",
                "category": "flexibility",
                "difficulty_level": "beginner",
                "estimated_duration": 20,
                "main_exercises": [
                    {
                        "name": "Sun Salutation A",
                        "duration": "2 minutes",
                        "rest": None,
                        "reps": "3 rounds",
                        "sets": 1
                    },
                    {
                        "name": "Warrior I Pose",
                        "duration": "30 seconds each side",
                        "rest": "10 seconds",
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Downward Dog",
                        "duration": "1 minute",
                        "rest": None,
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Child's Pose",
                        "duration": "1 minute",
                        "rest": None,
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Seated Meditation",
                        "duration": "5 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    }
                ],
                "equipment_needed": ["yoga_mat"],
                "calories_estimate": 80,
                "motivation_tip": "Move slowly and focus on your breath. Hold each pose with intention and listen to your body.",
                "form_tips": ["Don't force any poses", "Use props if needed", "Focus on breathing deeply"],
                "video_url": "https://example.com/yoga-flow",
                "thumbnail_url": "https://example.com/yoga-image.jpg",
                "featured": False,
                "date": date.today() + timedelta(days=1)
            },
            {
                "title": "Upper Body Strength Builder",
                "description": "Focused strength training for arms, chest, shoulders, and back. Build muscle and improve definition.",
                "category": "strength",
                "difficulty_level": "intermediate",
                "estimated_duration": 45,
                "main_exercises": [
                    {
                        "name": "Push-ups",
                        "duration": None,
                        "rest": "60 seconds",
                        "reps": "12-15",
                        "sets": 4
                    },
                    {
                        "name": "Dumbbell Rows",
                        "duration": None,
                        "rest": "60 seconds",
                        "reps": "10-12 each arm",
                        "sets": 3
                    },
                    {
                        "name": "Shoulder Press",
                        "duration": None,
                        "rest": "60 seconds",
                        "reps": "10-12",
                        "sets": 3
                    },
                    {
                        "name": "Bicep Curls",
                        "duration": None,
                        "rest": "45 seconds",
                        "reps": "12-15",
                        "sets": 3
                    },
                    {
                        "name": "Tricep Dips",
                        "duration": None,
                        "rest": "60 seconds",
                        "reps": "8-12",
                        "sets": 3
                    },
                    {
                        "name": "Plank",
                        "duration": "30-60 seconds",
                        "rest": "60 seconds",
                        "reps": None,
                        "sets": 3
                    }
                ],
                "equipment_needed": ["dumbbells", "bench"],
                "calories_estimate": 280,
                "motivation_tip": "Focus on controlled movements and proper form. Increase weight progressively. Rest adequately between sets.",
                "form_tips": ["Warm up properly before lifting", "Keep core engaged throughout", "Progressive overload is key"],
                "video_url": "https://example.com/upper-body-strength",
                "thumbnail_url": "https://example.com/strength-image.jpg",
                "featured": True,
                "date": date.today() + timedelta(days=2)
            },
            {
                "title": "Cardio Dance Party",
                "description": "Fun, high-energy dance workout that will get your heart pumping and put a smile on your face!",
                "category": "cardio",
                "difficulty_level": "beginner",
                "estimated_duration": 25,
                "main_exercises": [
                    {
                        "name": "Warm-up Dance",
                        "duration": "3 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    },
                    {
                        "name": "Hip Hop Sequence",
                        "duration": "4 minutes",
                        "rest": "30 seconds",
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Latin Dance Mix",
                        "duration": "4 minutes",
                        "rest": "30 seconds",
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Freestyle Dance",
                        "duration": "3 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Cool Down Stretch",
                        "duration": "4 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    }
                ],
                "equipment_needed": ["none"],
                "calories_estimate": 200,
                "motivation_tip": "Follow the rhythm and have fun! Don't worry about perfect moves, just keep moving and enjoy.",
                "form_tips": ["Wear comfortable shoes", "Stay hydrated", "Let loose and enjoy the music!"],
                "video_url": "https://example.com/dance-cardio",
                "thumbnail_url": "https://example.com/dance-image.jpg",
                "featured": False,
                "date": date.today() + timedelta(days=3)
            },
            {
                "title": "Lower Body Power",
                "description": "Explosive lower body workout focusing on legs and glutes. Build strength, power, and definition.",
                "category": "strength",
                "difficulty_level": "advanced",
                "estimated_duration": 40,
                "main_exercises": [
                    {
                        "name": "Goblet Squats",
                        "duration": None,
                        "rest": "60 seconds",
                        "reps": "15-20",
                        "sets": 4
                    },
                    {
                        "name": "Bulgarian Split Squats",
                        "duration": None,
                        "rest": "60 seconds",
                        "reps": "12 each leg",
                        "sets": 3
                    },
                    {
                        "name": "Deadlifts",
                        "duration": None,
                        "rest": "90 seconds",
                        "reps": "8-10",
                        "sets": 4
                    },
                    {
                        "name": "Jump Squats",
                        "duration": "30 seconds",
                        "rest": "30 seconds",
                        "reps": None,
                        "sets": 4
                    },
                    {
                        "name": "Walking Lunges",
                        "duration": None,
                        "rest": "45 seconds",
                        "reps": "20 total",
                        "sets": 3
                    },
                    {
                        "name": "Calf Raises",
                        "duration": None,
                        "rest": "30 seconds",
                        "reps": "20-25",
                        "sets": 3
                    }
                ],
                "equipment_needed": ["dumbbells", "kettlebell"],
                "calories_estimate": 320,
                "motivation_tip": "Focus on explosive movements during concentric phase, controlled during eccentric. Maintain proper knee alignment.",
                "form_tips": ["Warm up thoroughly", "Keep chest up during squats", "Land softly on jumps"],
                "video_url": "https://example.com/lower-body-power",
                "thumbnail_url": "https://example.com/legs-image.jpg",
                "featured": True,
                "date": date.today() + timedelta(days=4)
            },
            {
                "title": "Recovery & Mobility",
                "description": "Gentle stretching and mobility work to help your muscles recover and maintain flexibility.",
                "category": "flexibility",
                "difficulty_level": "beginner",
                "estimated_duration": 30,
                "main_exercises": [
                    {
                        "name": "Full Body Dynamic Warm-up",
                        "duration": "5 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    },
                    {
                        "name": "Hip Flexor Stretch",
                        "duration": "45 seconds each side",
                        "rest": "15 seconds",
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Hamstring Stretch",
                        "duration": "45 seconds each leg",
                        "rest": "15 seconds",
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Shoulder Circles & Stretches",
                        "duration": "2 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Spinal Twists",
                        "duration": "30 seconds each side",
                        "rest": "10 seconds",
                        "reps": None,
                        "sets": 2
                    },
                    {
                        "name": "Relaxation & Deep Breathing",
                        "duration": "5 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    }
                ],
                "equipment_needed": ["yoga_mat"],
                "calories_estimate": 60,
                "motivation_tip": "Hold stretches gently without bouncing. Breathe deeply and relax into each position.",
                "form_tips": ["Never force a stretch", "Focus on relaxation", "This is recovery time for your body"],
                "video_url": "https://example.com/recovery-mobility",
                "thumbnail_url": "https://example.com/recovery-image.jpg",
                "featured": False,
                "date": date.today() + timedelta(days=5)
            },
            {
                "title": "Weekend Warrior Full Body",
                "description": "Complete full-body workout combining strength, cardio, and flexibility. Perfect for weekend sessions.",
                "category": "full_body",
                "difficulty_level": "intermediate",
                "estimated_duration": 50,
                "main_exercises": [
                    {
                        "name": "Dynamic Warm-up",
                        "duration": "5 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    },
                    {
                        "name": "Circuit 1: Push-ups, Squats, Plank",
                        "duration": "45 seconds each",
                        "rest": "15 seconds between, 2 min between rounds",
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Circuit 2: Burpees, Lunges, Russian Twists",
                        "duration": "40 seconds each",
                        "rest": "20 seconds between, 2 min between rounds",
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Circuit 3: Jump Squats, Pike Push-ups, Bicycle Crunches",
                        "duration": "35 seconds each",
                        "rest": "25 seconds between, 2 min between rounds",
                        "reps": None,
                        "sets": 3
                    },
                    {
                        "name": "Cool Down Stretching",
                        "duration": "8 minutes",
                        "rest": None,
                        "reps": None,
                        "sets": 1
                    }
                ],
                "equipment_needed": ["none"],
                "calories_estimate": 400,
                "motivation_tip": "Complete each circuit fully before moving to the next. Maintain intensity but listen to your body.",
                "form_tips": ["Stay hydrated throughout", "Modify exercises as needed", "Focus on form over speed"],
                "video_url": "https://example.com/weekend-warrior",
                "thumbnail_url": "https://example.com/fullbody-image.jpg",
                "featured": True,
                "date": date.today() + timedelta(days=6)
            }
        ]
        
        # Create workout objects
        for workout_data in workouts:
            workout = WorkoutOfTheDay(**workout_data)
            db.add(workout)
        
        db.commit()
        print(f"✅ Successfully created {len(workouts)} sample workouts!")
        
        # Print summary
        print("\n📋 Workouts created:")
        for i, workout in enumerate(workouts, 1):
            print(f"{i}. {workout['title']} ({workout['category']}, {workout['difficulty_level']}) - {workout['estimated_duration']} min")
        
    except Exception as e:
        print(f"❌ Error creating workouts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🏋️ Creating sample workouts for FitMotiv...")
    create_sample_workouts()
    print("✅ Workout population completed!")