from app.agent.planner import generate_plan

steps = generate_plan("系统解释 JVM GC 的分代收集机制")
print(steps)
