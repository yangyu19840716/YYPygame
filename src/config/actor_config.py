# -*- coding:utf-8 -*-

from enum import Enum
from typing import Dict, List, Set


class ActorType(Enum):
    NORMAL = "normal"
    LEADER = "leader"


class ActorConfig:
    ACTOR_NUM = 100
    LEADER_RATIO = 0.05
    
    RULE_ASSIGNMENTS = {
        ActorType.NORMAL: [
            'FollowNearestLeaderRule',
            'CollisionAvoidanceRule'
        ],
        ActorType.LEADER: [
            'LeaderRandomMovementRule',
            'FollowNearestLeaderRule',
            'CollisionAvoidanceRule'
        ]
    }
    
    @classmethod
    def get_leader_count(cls) -> int:
        return int(cls.ACTOR_NUM * cls.LEADER_RATIO)
    
    @classmethod
    def get_normal_count(cls) -> int:
        return cls.ACTOR_NUM - cls.get_leader_count()
    
    @classmethod
    def get_rules_for_type(cls, actor_type: ActorType) -> List[str]:
        return cls.RULE_ASSIGNMENTS.get(actor_type, [])
    
    @classmethod
    def get_all_rules(cls) -> Set[str]:
        all_rules = set()
        for rules in cls.RULE_ASSIGNMENTS.values():
            all_rules.update(rules)
        return all_rules