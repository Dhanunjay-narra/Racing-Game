import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from backend.database.session import Base


class VehicleCatalog(Base):
    __tablename__ = "vehicle_catalog"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(50), nullable=False)
    category = Column(String(30), nullable=False)
    tier = Column(Integer, default=1, nullable=False)
    rarity = Column(String(20), default="Common")
    
    base_speed = Column(Float, nullable=False)
    base_acceleration = Column(Float, nullable=False)
    base_handling = Column(Float, nullable=False)
    base_braking = Column(Float, nullable=False)
    base_drift = Column(Float, nullable=False)
    base_weight_kg = Column(Float, nullable=False)
    drivetrain = Column(String(10), default="RWD")
    engine_type = Column(String(30), default="V8 Twin-Turbo")
    max_rpm = Column(Integer, default=8500)
    gear_count = Column(Integer, default=6)
    
    purchase_price_credits = Column(Integer, default=25000)
    purchase_price_gold = Column(Integer, default=0)
    is_purchasable = Column(Boolean, default=True)
    model_3d_path = Column(String(255), nullable=False)
    thumbnail_path = Column(String(255), nullable=False)


class PlayerVehicle(Base):
    __tablename__ = "player_vehicles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    catalog_vehicle_id = Column(String(50), ForeignKey("vehicle_catalog.id"), nullable=False)
    
    engine_level = Column(Integer, default=1, nullable=False)
    transmission_level = Column(Integer, default=1, nullable=False)
    brakes_level = Column(Integer, default=1, nullable=False)
    tires_level = Column(Integer, default=1, nullable=False)
    suspension_level = Column(Integer, default=1, nullable=False)
    aero_level = Column(Integer, default=1, nullable=False)
    turbo_level = Column(Integer, default=1, nullable=False)
    nitro_level = Column(Integer, default=1, nullable=False)
    weight_reduction_level = Column(Integer, default=1, nullable=False)
    
    paint_color = Column(String(20), default="#FF0044")
    paint_finish = Column(String(20), default="Gloss")
    decal_id = Column(String(50), default="none")
    rim_color = Column(String(20), default="#111111")
    spoiler_id = Column(String(50), default="stock")
    window_tint_opacity = Column(Float, default=0.2)
    underglow_color = Column(String(20), default="none")
    license_plate_text = Column(String(10), default="NEXUS")
    
    mastery_xp = Column(Integer, default=0)
    mastery_level = Column(Integer, default=1)
    kilometers_driven = Column(Float, default=0.0)
    races_won = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)
    acquired_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="garage_vehicles")
    catalog_spec = relationship("VehicleCatalog")
