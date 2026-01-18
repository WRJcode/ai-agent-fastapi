from app.agent.memory import ShortTermMemory

mem = ShortTermMemory(max_turns=2)

mem.add_user_message("什么是 JVM GC？")
mem.add_assistant_message("GC 是垃圾回收机制")

mem.add_user_message("那分代收集呢？")

for m in mem.get_context():
    print(m)
