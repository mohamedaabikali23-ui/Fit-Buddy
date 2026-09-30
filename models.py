"""
FitBuddy - SQLAlchemy Data Models
Defines schema for User Profiles, Generated Workout Routines,
Precision Meal Blueprints, and Conversational Coach Messages.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), default="Athlete")
    age = Column(Integer, default=28)
    gender = Column(String(20), default="Male")
    height_cm = Column(Float, default=178.0)
    weight_kg = Column(Float, default=85.0)
    target_weight_kg = Column(Float, default=75.0)
    goal = Column(String(100), default="Fat Loss / Caloric Deficit")
    activity_level = Column(String(100), default="Moderately Active (3-5 days exercise/week)")
    experience = Column(String(50), default="Intermediate")
    equipment = Column(String(100), default="Full Gym Access")
    days_per_week = Column(Integer, default=4)
    session_duration_mins = Column(Integer, default=45)
    diet_type = Column(String(100), default="High Protein Omnivore")
    allergies = Column(String(255), default="None")
    injuries = Column(String(255), default="Minor knee stiffness on deep squats")

    # Calculated Biometrics & Metabolic Numbers
    bmi = Column(Float, default=26.8)
    bmi_category = Column(String(50), default="Overweight (Pre-obese)")
    bmr = Column(Integer, default=1820)
    tdee = Column(Integer, default=2821)
    target_calories = Column(Integer, default=2321)
    calorie_mode = Column(String(50), default="Deficit (-500 kcal)")
    protein_g = Column(Integer, default=170)
    carbs_g = Column(Integer, default=232)
    fat_g = Column(Integer, default=77)
    hydration_l = Column(Float, default=3.3)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workouts = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    title = Column(String(200), default="Personalized Weekly Training Split")
    goal = Column(String(100), default="General Fitness")
    content_markdown = Column(Text, nullable=False)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="workouts")


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    title = Column(String(200), default="Personalized Daily Macro Blueprint")
    calorie_target = Column(Integer, default=2000)
    content_markdown = Column(Text, nullable=False)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="meals")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="chat_messages")
