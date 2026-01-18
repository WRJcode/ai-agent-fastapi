from app.agent.memory import LongTermMemory

mem = LongTermMemory()

mem.add("Java 的垃圾回收采用分代收集策略")
mem.add("新生代主要使用复制算法")
mem.add("老年代常用标记-整理算法")

results = mem.search("JVM GC 是怎么分代的？")

print("检索结果：")
for r in results:
    print("-", r)
