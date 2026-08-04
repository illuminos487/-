import random

# ==========================================
# 🎲 전용장비 조율 시뮬레이터 (파이썬 버전)
# ==========================================

TIERS = ['고급', '희귀', '전설']
TIER_WEIGHTS = [45, 35, 20]
OPTIONS = [
    '모든 공격력(%)', '방어력(%)', '생명력(%)', '효과 적중', 
    '효과 저항', '피해 증폭', '파쇄', '탄성', '재생'
]
STATS = {
    '고급': ['5%', '5%', '5%', '4%', '4%', '1.6%', '4.8%', '6%', '2.4%'],
    '희귀': ['7%', '7%', '7%', '6%', '6%', '2.4%', '7.2%', '9%', '3.6%'],
    '전설': ['12%', '12%', '12%', '10%', '10%', '4%', '12%', '15%', '6%']
}

def roll_tuning(current_tier, current_option):
    """단일 슬롯 조율 롤링 함수"""
    while True:
        rolled_tier = random.choices(TIERS, weights=TIER_WEIGHTS, k=1)[0]
        rolled_option_idx = random.randint(0, 8)
        rolled_option = OPTIONS[rolled_option_idx]
        
        # 현재 옵션과 완전히 동일하면 재추첨 (게임 룰)
        if rolled_tier == current_tier and rolled_option == current_option:
            continue
            
        return rolled_tier, rolled_option, STATS[rolled_tier][rolled_option_idx]

class TuningSimulator:
    def __init__(self):
        # 4개의 부위 슬롯 초기화
        self.slots = [{'tier': None, 'option': None, 'stat': None, 'is_locked': False} for _ in range(4)]
        self.total_attempts = 0

    def get_stones_used(self):
        return self.total_attempts * 50

    def roll_slot(self, index):
        """특정 슬롯 1회 조율"""
        slot = self.slots[index]
        if slot['is_locked']:
            return False
        
        tier, option, stat = roll_tuning(slot['tier'], slot['option'])
        slot['tier'] = tier
        slot['option'] = option
        slot['stat'] = stat
        self.total_attempts += 1
        return True

    def display_status(self):
        """현재 슬롯 상태 출력"""
        print(f"\n--- 📊 최종 결과 ---")
        print(f"총 시도: {self.total_attempts:,}회 | 소모 조율석: {self.get_stones_used():,}개")
        for i, slot in enumerate(self.slots):
            lock_str = "🔒 잠금" if slot['is_locked'] else "🔓"
            if slot['tier'] is None:
                print(f"부위 {i+1} [{lock_str}]: 빈 슬롯")
            else:
                print(f"부위 {i+1} [{lock_str}]: [{slot['tier']}] {slot['option']} ({slot['stat']})")
        print("-" * 40)

    def auto_tune(self, targets, max_cycles=1000000):
        """
        4부위 동시 오토 조율 (천장 시스템)
        targets 예시: [{'tier': '전설', 'option': '모든 공격력(%)'}, ...]
        """
        cycles = 0
        
        while cycles < max_cycles:
            all_met = True
            
            for i in range(4):
                if not self.slots[i]['is_locked']:
                    self.roll_slot(i)
                    
                    target_tier = targets[i]['tier']
                    target_option = targets[i]['option']
                    curr_tier = self.slots[i]['tier']
                    curr_option = self.slots[i]['option']
                    
                    # 1. 등급 체크 로직
                    match_tier = False
                    if target_tier == 'ANY':
                        match_tier = True
                    elif target_tier == '전설/희귀':
                        match_tier = (curr_tier in ['전설', '희귀'])
                    else:
                        match_tier = (curr_tier == target_tier)
                        
                    # 2. 옵션 체크 로직
                    match_option = (target_option == 'ANY' or curr_option == target_option)
                    
                    # 조건 달성 시 즉시 잠금
                    if match_tier and match_option:
                        self.slots[i]['is_locked'] = True
                    else:
                        all_met = False
            
            cycles += 1
            if all_met:
                break
        
        if not all_met:
            print(f"\n[경고] 최대 사이클({max_cycles}회)에 도달했지만 모든 목표를 달성하지 못했습니다.")

# ==========================================
# 🚀 실행 예시 (직접 수정해서 테스트 가능)
# ==========================================
if __name__ == "__main__":
    sim = TuningSimulator()
    
    # 목표 설정 (ANY: 상관없음, 전설/희귀: 고급 제외)
    targets = [
        {'tier': '전설', 'option': '모든 공격력(%)'},     # 1번 부위 목표
        {'tier': '전설/희귀', 'option': '파쇄'},          # 2번 부위 목표
        {'tier': 'ANY', 'option': '방어력(%)'},          # 3번 부위 목표
        {'tier': '전설', 'option': 'ANY'}                # 4번 부위 목표
    ]
    
    print("🤖 4부위 동시 자동 조율을 시작합니다...")
    sim.auto_tune(targets)
    sim.display_status()
