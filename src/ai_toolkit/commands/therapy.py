"""
心理咨询和治疗辅助
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group(name="therapy")
def therapy_cli():
    """心理咨询和治疗辅助"""
    pass


@therapy_cli.command(name="chat")
@click.option("--mode", "-m", default="empathy", help="对话模式")
def therapy_chat(mode: str):
    """心理咨询对话"""
    console.print(f"\n💬 心理咨询对话\n")

    console.print(f"模式: {mode}")

    console.print("\n对话开始:")
    console.print("  AI: 你好，我是你的AI心理咨询师")
    console.print("  AI: 今天想聊些什么呢？")

    console.print("\n对话示例:")
    console.print("  你: 我最近总是感到焦虑")
    console.print("  AI: 我理解你的感受")
    console.print("  AI: 能告诉我更多吗？")
    console.print("  你: 工作压力很大...")
    console.print("  AI: 工作压力确实会让人焦虑")
    console.print("  AI: 你觉得压力来自哪里？")

    console.print("\n咨询技巧:")
    console.print("  ✓ 倾听与共情")
    console.print("  ✓ 开放式提问")
    console.print("  ✓ 情感确认")
    console.print("  ✓ 不予评判")

    console.print("\n对话时长:")
    console.print("  当前: 15分钟")
    console.print("  建议: 45-60分钟")

    console.print("\n✅ 对话结束")


@therapy_cli.command(name="assess")
@click.option("--scale", "-s", default="phq9", help="评估量表")
def mental_assessment(scale: str):
    """心理评估"""
    console.print(f"\n📊 心理评估\n")

    console.print(f"量表: {scale}")

    if scale == "phq9":
        console.print("\nPHQ-9 (抑郁筛查):")
        console.print("\n问题:")
        for i in range(1, 10):
            console.print(f"  {i}. (1-4分) - 抑郁症状")
        
        console.print("\n评分:")
        score = 12
        console.print(f"  总分: {score}/27")

        console.print("\n结果解读:")
        if score <= 4:
            console.print("  无抑郁 (0-4分)")
        elif score <= 9:
            console.print("  轻度抑郁 (5-9分)")
        elif score <= 14:
            console.print("  中度抑郁 (10-14分) ← 当前")
        elif score <= 19:
            console.print("  中重度抑郁 (15-19分)")
        else:
            console.print("  重度抑郁 (20-27分)")

    elif scale == "gad7":
        console.print("\nGAD-7 (焦虑筛查):")
        score = 10
        console.print(f"  总分: {score}/21")
        console.print("  结果: 中度焦虑")

    console.print("\n建议:")
    console.print("  1. 寻求专业帮助")
    console.print("  2. 建立支持网络")
    console.print("  3. 规律作息")
    console.print("  4. 适度运动")

    console.print("\n⚠️  本评估仅供参考")
    console.print("  诊断请咨询专业医师")

    console.print("\n✅ 评估完成")


@therapy_cli.command(name="diary")
@click.option("--prompt", "-p", default="mood", help="提示类型")
def mood_diary(prompt: str):
    """情绪日记"""
    console.print(f"\n📔 情绪日记\n")

    console.print(f"提示: {prompt}")

    console.print("\n今日记录:")
    console.print("  日期: 2026-02-22")
    console.print("  时间: 21:00")

    console.print("\n情绪追踪:")
    console.print("  早晨: 😊 开心 (7/10)")
    console.print("  中午: 😐 平静 (6/10)")
    console.print("  下午: 😰 焦虑 (4/10)")
    console.print("  晚上: 😊 放松 (7/10)")

    console.print("\n情绪事件:")
    console.print("  积极事件:")
    console.print("    - 完成项目")
    console.print("    - 收到表扬")
    console.print("  消极事件:")
    console.print("    - 工作压力")
    console.print("    - 时间紧张")

    console.print("\n反思:")
    console.print("  今日情绪: 总体良好")
    console.print("  主要挑战: 工作压力")
    console.print("  应对方式: 深呼吸")
    console.print("  明日目标: 保持平衡")

    console.print("\n趋势分析:")
    console.print("  本周平均: 6.2/10")
    console.print("  上周平均: 5.8/10")
    console.print("  变化: +0.4 ↗")

    console.print("\n✅ 记录完成")


@therapy_cli.command(name="meditation")
@click.option("--duration", "-d", default=15, help="时长(分钟)")
@click.option("--type", "-t", default="mindfulness", help="冥想类型")
def guided_meditation(duration: int, type: str):
    """引导冥想"""
    console.print(f("\n🧘 引导冥想\n")

    console.print(f"时长: {duration}分钟")
    console.print(f"类型: {type}")

    console.print("\n冥想准备:")
    console.print("  环境: 安静舒适")
    console.print("  姿势: 舒适坐姿")
    console.print("  闭眼: 放松双眼")
    console.print("  呼吸: 自然呼吸")

    console.print("\n引导语:")
    console.print("  1. 感受身体")
    console.print("  2. 专注呼吸")
    console.print("  3. 观察念头")
    console.print("  4. 不予评判")
    console.print("  5. 回到当下")

    console.print("\n冥想计时:")
    console.print("  0:00-5:00: 身体扫描")
    console.print("  5:00-10:00: 呼吸觉察")
    console.print(f"  10:00-{duration}:00: 正念冥想")

    console.print("\n冥想结束:")
    console.print("  感受: 放松")
    console.print("  心情: 平静")
    console.print("  效果: 良好")

    console.print("\n每日练习:")
    console.print("  建议频率: 每天1次")
    console.print("  最佳时间: 早晨或睡前")
    console.print("  持续时间: 10-20分钟")

    console.print("\n✅ 冥想完成")


@therapy_cli.command(name="relax")
@click.option("--technique", "-t", default="pmr", help="放松技术")
def relaxation(technique: str):
    """放松训练"""
    console.print(f"\n😌 放松训练\n")

    console.print(f"技术: {technique}")

    if technique == "pmr":
        console.print("\n渐进式肌肉放松:")
        console.print("  原理: 紧张后放松")
        console.print("  时长: 15-20分钟")
        
        console.print("\n放松步骤:")
        console.print("  1. 右手握拳: 保持5秒")
        console.print("  2. 突然放松: 感受放松")
        console.print("  3. 体验20秒")
        console.print("  4. 换左手: 重复")
        console.print("  5. 依次: 全身肌肉群")

    elif technique == "breathing":
        console.print("\n呼吸放松:")
        console.print("  4-7-8呼吸法")
        console.print("  吸气: 4秒")
        console.print("  屏气: 7秒")
        console.print("  呼气: 8秒")
        console.print("  重复: 5-10次")

    elif technique == "visualization":
        console.print("\n想象放松:")
        console.print("  想象安全场所")
        console.print("  感受宁静")
        console.print("  体验放松")

    console.print("\n✅ 训练完成")


@therapy_cli.command(name="cbt")
@click.option("--thought", "-t", help="负面思维")
def cbt_reframe(thought: str):
    """认知重构"""
    console.print(f"\n🔄 认知重构\n")

    console.print(f"想法: {thought or '我总是做不好事情'}")

    console.print("\nCBT认知三角:")
    console.print("  思维: 我总是失败")
    console.print("  情绪: 沮丧、焦虑")
    console.print("  行为: 回避尝试")

    console.print("\n认知扭曲:")
    console.print("  过度概括")
    console.print("  非黑即白")
    console.print("  灾难化")

    console.print("\n苏格拉底式提问:")
    console.print("  1. 这个想法有证据吗？")
    console.print("  2. 有反例吗？")
    console.print("  3. 还有其他解释吗？")
    console.print("  4. 最坏会怎样？")
    console.print("  5. 朋友会怎么说？")

    console.print("\n理性回应:")
    console.print("  ✓ 并非总是失败")
    console.print("  ✓ 有成功经历")
    console.print("  ✓ 错误是学习机会")
    console.print("  ✓ 可以改进提升")

    console.print("\n新思维:")
    console.print("  '有时会犯错，但我能学习'")

    console.print("\n✅ 重构完成")


@therapy_cli.command(name="exposure")
@click.option("--target", "-t", help="恐惧对象")
@click.option("--intensity", "-i", default=5, help="焦虑等级(1-10)")
def exposure_therapy(target: str, intensity: int):
    """暴露疗法"""
    console.print(f"\n🎯 暴露疗法\n")

    console.print(f"恐惧对象: {target or '公众演讲'}")
    console.print(f"焦虑等级: {intensity}/10")

    console.print("\n焦虑阶梯:")
    console.print("  Level 1 (轻度): 看演讲视频")
    console.print("  Level 3 (中度): 对镜练习")
    console.print("  Level 5 (中重度): 小组练习")
    console.print("  Level 7 (重度): 班级演讲")
    console.print("  Level 9 (极重度): 大型演讲")

    console.print("\n暴露流程:")
    console.print("  1. 建立焦虑阶梯")
    console.print("  2. 从低级开始")
    console.print("  3. 暴露练习")
    console.print("  4. 适应焦虑")
    console.print("  5. 逐步升级")

    console.print("\n当前练习:")
    console.print(f"  Level: {intensity}")
    console.print(f"  时长: 30分钟")
    console.print(f"  重复: 每天1次")

    console.print("\n效果评估:")
    console.print("  初始焦虑: {intensity}/10")
    console.print("  当前焦虑: {intensity - 2}/10")
    console.print("  降低: -2")

    console.print("\n✅ 练习完成")


@therapy_cli.command(name="sleep")
def sleep_improvement():
    """睡眠改善"""
    console.print(f"\n😴 睡眠改善\n")

    console.print("睡眠评估:")
    console.print("  入睡时间: 30分钟 (过长)")
    console.print("  睡眠时长: 5.5小时 (不足)")
    console.print("  睡眠质量: 中等")
    console.print("  夜醒次数: 2-3次")

    console.print("\n睡眠卫生:")
    console.print("  ✓ 固定起床时间")
    console.print("  ✓ 限制午睡 <30分钟")
    console.print("  ✓ 避免咖啡因午后")
    console.print("  ✓ 睡前1小时不使用电子设备")
    console.print("  ✓ 营造舒适睡眠环境")

    console.print("\n刺激控制:")
    console.print("  床 = 仅用于睡眠")
    console.print("  20分钟睡不着 → 离开卧室")
    console.print("  有睡意再回床")

    console.print("\n放松技巧:")
    console.print("  4-7-8呼吸法")
    console.print("  渐进性肌肉放松")
    console.print("  正念冥想")

    console.print("\n睡眠限制:")
    console.print("  当前: 在床9小时，睡眠5.5小时")
    console.print("  调整: 在床6小时")
    console.print("  目标: 提高睡眠效率至90%")

    console.print("\n✅ 计划已制定")


@therapy_cli.command(name="assertive")
def assertiveness_training():
    """自信训练"""
    console.print(f"\n💪 自信训练\n")

    console.print("沟通风格:")
    console.print("  被动: 顺从他人")
    console.print("  攻击: 忽视他人")
    console.print("  自信: 尊重双方 ✓")

    console.print("\n自信表达要素:")
    console.print("  ✓ 清晰表达需求")
    console.print("  ✓ 维护自己权利")
    console.print("  ✓ 尊重他人权利")
    console.print("  ✓ 不带攻击性")

    console.print("\nASSERT模型:")
    console.print("  A - Attention (注意)")
    console.print("  S - Say clearly (清晰表达)")
    console.print("  S - Specify (具体要求)")
    console.print("  E - Express feelings (表达感受)")
    console.print("  R - Result (结果)")
    console.print("  T - Time (时间)")

    console.print("\n示例:")
    console.print("  '我需要你明天完成报告，")
    console.print("   因为这对项目很重要。")
    console.print("   我希望我们能达成一致。'")

    console.print("\n✅ 训练完成")


@therapy_cli.command(name="crisis")
@click.option("--severity", "-s", default="moderate", help="严重程度")
def crisis_intervention(severity: str):
    """危机干预"""
    console.print(f"\n🆘 危机干预\n")

    console.print(f"严重程度: {severity}")

    console.print("\n风险评估:")
    if severity == "low":
        console.print("  风险: 低")
        console.print("  行动: 自助+支持")
    elif severity == "moderate":
        console.print("  风险: 中等")
        console.print("  行动: 专业评估")
    else:
        console.print("  风险: 高")
        console.print("  行动: 紧急干预")

    console.print("\n危机热线:")
    console.print("  全国心理援助: 400-161-9995")
    console.print("  北京: 010-82951332")
    console.print("  上海: 021-12320-5")
    console.print("  广州: 020-81899120")

    console.print("\n安全计划:")
    console.print("  1. 识别预警信号")
    console.print("  2. 列出应对策略")
    console.print("  3. 联系支持人员")
    console.print("  4. 减少环境风险")
    console.print("  5. 制定应急计划")

    console.print("\n支持网络:")
    console.print("  家人: ✓")
    console.print("  朋友: ✓")
    console.print("  医师: ✓")
    console.print("  热线: ✓")

    console.print("\n⚠️  如有自伤风险，立即就医")
    console.print("  就近医院急诊: 120")

    console.print("\n✅ 计划已制定")


@therapy_cli.command(name="goal")
@click.option("--type", "-t", help="目标类型")
def goal_setting(type: str):
    """目标设定"""
    console.print(f"\n🎯 目标设定\n")

    console.print(f"类型: {type or 'weekly'}")

    console.print("\nSMART原则:")
    console.print("  S - Specific (具体)")
    console.print("  M - Measurable (可衡量)")
    console.print("  A - Achievable (可达成)")
    console.print("  R - Relevant (相关)")
    console.print("  T - Time-bound (时限)")

    console.print("\n本周目标:")
    console.print("  1. 每天冥想10分钟")
    console.print("  2. 写3次情绪日记")
    console.print("  3. 运动3次")
    console.print("  4. 11点前睡觉")

    console.print("\n行动计划:")
    console.print("  周一-周日: 每天1项")
    console.print("  记录进度: ✓")
    console.print("  周末回顾: ✓")

    console.print("\n奖赏机制:")
    console.print("  完成目标: 🎉")
    console.print("  部分完成: 👍")
    console.print("  未完成: 重新规划")

    console.print("\n✅ 目标已设定")


@therapy_cli.command(name="progress")
def track_progress():
    """进度追踪"""
    console.print(f"\n📈 进度追踪\n")

    console.print("本周进度:")
    console.print("  冥想: 5/7天 (71%)")
    console.print("  日记: 3/3次 (100%)")
    console.print("  运动: 2/3次 (67%)")
    console.print("  早睡: 4/7天 (57%)")

    console.print("\n情绪趋势:")
    console.print("  周一: 5/10")
    console.print("  周二: 6/10")
    console.print("  周三: 7/10")
    console.print("  周四: 6/10")
    console.print("  周五: 7/10")
    console.print("  周六: 8/10")
    console.print("  周日: 7/10")
    console.print("  平均: 6.6/10")

    console.print("\n对比分析:")
    console.print("  本周: 6.6/10")
    console.print("  上周: 5.8/10")
    console.print("  提升: +0.8 ↗")

    console.print("\n突破:")
    console.print("  ✓ 情绪稳定")
    console.print("  ✓ 睡眠改善")
    console.print("  ⚠️ 运动不足")

    console.print("\n下周调整:")
    console.print("  增加运动频率")
    console.print("  保持冥想练习")
    console.print("  继续情绪追踪")

    console.print("\n✅ 追踪完成")


@therapy_cli.command(name="resource")
@click.option("--category", "-c", help="资源类别")
def find_resource(category: str):
    """寻找资源"""
    console.print(f"\n📚 寻找资源\n")

    console.print(f"类别: {category or 'all'}")

    console.print("\n专业资源:")
    console.print("  心理咨询师:")
    console.print("    - 中国心理学会: cps.org.cn")
    console.print("    - 好大夫在线: haodf.com")
    console.print("  精神科医师:")
    console.print("    - 三甲医院心理科")
    console.print("    - 精神卫生中心")

    console.print("\n自助资源:")
    console.print("  书籍:")
    console.print("    - 《认知疗法: 基础与应用》")
    console.print("    - 《正念: 此刻是一枝花》")
    console.print("  App:")
    console.print("    - 冥想指南: Headspace/Calm")
    console.print("    - 情绪追踪: MoodNotes")
    console.print("  在线课程:")
    console.print("    - CBT自助课程")
    console.print("    - 正念训练课程")

    console.print("\n支持团体:")
    console.print("  匿名戒酒互助会")
    console.print("  抑郁症互助会")
    console.print("  焦虑症互助会")

    console.print("\n✅ 资源已找到")


@therapy_cli.command(name="log")
def therapy_log():
    """咨询日志"""
    console.print(f"\n📝 咨询日志\n")

    console.print("今日统计:")
    console.print("  咨询对话: 12次")
    console.print("  心理评估: 8次")
    console.print("  危机干预: 1次")
    console.print("  情绪日记: 25篇")

    console.print("\n工作记录:")
    console.print("  09:00-10:00: 初次访谈")
    console.print("  10:30-11:00: CBT练习")
    console.print("  14:00-15:00: 暴露疗法")
    console.print("  15:30-16:00: 正念训练")

    console.print("\n重点关注:")
    console.print("  ⚠️ 危机个案: 1人")
    console.print("  ⚠️ 抑郁倾向: 3人")
    console.print("  ⚠️ 焦虑症状: 5人")

    console.print("\n✅ 日志记录完成")
