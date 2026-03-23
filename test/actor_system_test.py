# -*- coding:utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.actor_config import ActorConfig, ActorType


def test_actor_config():
    print("=== Actor Configuration Test ===")
    print(f"Total Actor Count: {ActorConfig.ACTOR_NUM}")
    print(f"Leader Ratio: {ActorConfig.LEADER_RATIO * 100}%")
    print(f"Expected Leader Count: {ActorConfig.get_leader_count()}")
    print(f"Expected Normal Count: {ActorConfig.get_normal_count()}")
    
    print("\n=== Rule Assignments ===")
    print(f"Normal Actor Rules: {ActorConfig.get_rules_for_type(ActorType.NORMAL)}")
    print(f"Leader Actor Rules: {ActorConfig.get_rules_for_type(ActorType.LEADER)}")
    
    print("\n=== All Rules ===")
    print(f"All Rules: {ActorConfig.get_all_rules()}")
    
    print("\n=== Verification ===")
    total = ActorConfig.get_leader_count() + ActorConfig.get_normal_count()
    expected_ratio = ActorConfig.get_leader_count() / ActorConfig.ACTOR_NUM
    print(f"Total Actors: {total} (Expected: {ActorConfig.ACTOR_NUM})")
    print(f"Actual Leader Ratio: {expected_ratio * 100:.2f}% (Expected: {ActorConfig.LEADER_RATIO * 100}%)")
    
    if total == ActorConfig.ACTOR_NUM:
        print("✅ Total actor count matches configuration")
    else:
        print("❌ Total actor count mismatch!")
    
    if abs(expected_ratio - ActorConfig.LEADER_RATIO) < 0.01:
        print("✅ Leader ratio matches configuration")
    else:
        print("❌ Leader ratio mismatch!")


def test_actor_creation():
    print("\n=== Actor Creation Test ===")
    
    from src.actor import Actor
    
    leader_count = 0
    normal_count = 0
    
    for i in range(10):
        actor = Actor(ActorType.LEADER)
        if actor.is_leader:
            leader_count += 1
        else:
            normal_count += 1
    
    for i in range(90):
        actor = Actor(ActorType.NORMAL)
        if actor.is_leader:
            leader_count += 1
        else:
            normal_count += 1
    
    print(f"Created Leaders: {leader_count} (Expected: 10)")
    print(f"Created Normal Actors: {normal_count} (Expected: 90)")
    
    if leader_count == 10 and normal_count == 90:
        print("✅ Actor creation test passed")
    else:
        print("❌ Actor creation test failed!")


def test_scene_creation():
    print("\n=== Scene Creation Test ===")
    
    from src.scene import Scene
    
    scene = Scene()
    
    leader_count = sum(1 for actor in scene.actors if actor.is_leader)
    normal_count = sum(1 for actor in scene.actors if not actor.is_leader)
    
    print(f"Scene Leaders: {leader_count} (Expected: {ActorConfig.get_leader_count()})")
    print(f"Scene Normal Actors: {normal_count} (Expected: {ActorConfig.get_normal_count()})")
    print(f"Total Actors: {len(scene.actors)} (Expected: {ActorConfig.ACTOR_NUM})")
    
    expected_leader = ActorConfig.get_leader_count()
    expected_normal = ActorConfig.get_normal_count()
    
    if leader_count == expected_leader and normal_count == expected_normal:
        print("✅ Scene creation test passed")
    else:
        print("❌ Scene creation test failed!")


if __name__ == "__main__":
    test_actor_config()
    test_actor_creation()
    test_scene_creation()
    
    print("\n=== All Tests Completed ===")