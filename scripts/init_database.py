#!/usr/bin/env python3
"""
Main initialization script for FitMotiv Backend
Populates database with sample data for all features
"""
import sys
import os
import subprocess
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_script(script_name, description):
    """Run a population script and handle errors"""
    print(f"\n🚀 {description}")
    print("=" * 50)
    
    try:
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, check=True)
        
        print(result.stdout)
        if result.stderr:
            print(f"⚠️ Warnings: {result.stderr}")
        
        print(f"✅ {description} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in {description}: {e}")
        return False

def main():
    """Initialize the entire FitMotiv database with sample data"""
    print("🎯 FitMotiv Backend Database Initialization")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # List of scripts to run in order
    initialization_steps = [
        ("populate_exercises.py", "Populating Exercise Database"),
        ("populate_motivation.py", "Populating Motivational Quotes"),
        ("populate_workouts.py", "Populating Workout of the Day"),
        ("populate_progress.py", "Populating Sample Progress Data"),
    ]
    
    success_count = 0
    total_steps = len(initialization_steps)
    
    print("📋 Initialization Plan:")
    for i, (script, description) in enumerate(initialization_steps, 1):
        print(f"   {i}. {description}")
    print()
    
    # Run each initialization script
    for i, (script, description) in enumerate(initialization_steps, 1):
        print(f"\n📍 Step {i}/{total_steps}")
        success = run_script(script, description)
        
        if success:
            success_count += 1
        else:
            response = input(f"\n⚠️ {description} failed. Continue with remaining steps? (y/n): ").lower()
            if response != 'y':
                print("🛑 Initialization stopped by user.")
                break
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 INITIALIZATION SUMMARY")
    print("=" * 60)
    print(f"✅ Completed: {success_count}/{total_steps} steps")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_steps:
        print("\n🎉 ALL INITIALIZATION STEPS COMPLETED SUCCESSFULLY!")
        print("\n📊 Your FitMotiv backend is now ready with:")
        print("   ✓ Exercise database with categorized workouts")
        print("   ✓ Daily motivational quotes")
        print("   ✓ Weekly workout schedules")
        print("   ✓ Sample user progress data")
        print("\n🚀 You can now start the API server with:")
        print("   python -m uvicorn app.main:app --reload")
        print("\n📖 API Documentation available at:")
        print("   http://localhost:8000/docs")
        
    else:
        print(f"\n⚠️ {total_steps - success_count} steps failed.")
        print("   Some features may not work properly.")
        print("   Check the errors above and re-run failed scripts manually.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()