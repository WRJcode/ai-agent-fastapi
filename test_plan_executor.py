from app.agent.plan_executor import PlanExecutor

executor = PlanExecutor()

results = executor.run("系统解释 JVM GC 的分代收集机制")

print("\n=== Observations ===")
for i, r in enumerate(results, start=1):
    print(f"\n--- Step {i} Result ---")
    print(r)
