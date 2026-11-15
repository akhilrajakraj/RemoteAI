import asyncio,json
from app.agents.definitions import AGENTS
from app.providers.base import ModelProvider
class MultiAgentOrchestrator:
    def __init__(self,provider:ModelProvider,max_parallel:int=3):
        self.provider=provider
        self.limit=asyncio.Semaphore(max(1,min(max_parallel,6)))
    def specialist(self,text:str)->str:
        t=text.lower()
        if any(x in t for x in ("python","code","debug","api","django","fastapi","sql","program")): return "developer"
        if any(x in t for x in ("plan","roadmap","schedule","steps","organise","organize")): return "planner"
        if any(x in t for x in ("write","email","rewrite","draft","resume","cover letter")): return "writer"
        if any(x in t for x in ("analyse","analyze","compare","data","calculate","decision")): return "analyst"
        if any(x in t for x in ("research","latest","explain","what is","why")): return "research"
        return "general"
    async def decompose(self,request:str):
        prompt=("Split this request only if it explicitly contains multiple independent deliverables. Return at most 3 tasks. "
        "Return JSON only: {\"tasks\":[{\"agent\":\"research|developer|planner|writer|analyst|general\",\"task\":\"...\"}]}. "
        "Otherwise return one task equal to the full request.\n"+request)
        try:
            raw=await self.provider.generate([{"role":"system","content":"You are a task router. Output valid JSON only."},{"role":"user","content":prompt}],temperature=0.1)
            items=json.loads(raw).get("tasks",[])
            valid=[{"agent":x["agent"],"task":str(x["task"]).strip()} for x in items[:3] if x.get("agent") in AGENTS and str(x.get("task","")).strip()]
            return valid or [{"agent":self.specialist(request),"task":request}]
        except (ValueError,TypeError,KeyError,AttributeError): return [{"agent":self.specialist(request),"task":request}]
    async def execute(self,item,history):
        agent=AGENTS[item["agent"]]
        messages=[{"role":"system","content":agent.prompt},*history[-12:],{"role":"user","content":item["task"]}]
        async with self.limit: return await self.provider.generate(messages)
    async def run(self,request:str,history:list[dict[str,str]]|None=None):
        tasks=await self.decompose(request)
        outcomes=await asyncio.gather(*(self.execute(t,history or []) for t in tasks),return_exceptions=True)
        results=[{"agent":t["agent"],"task":t["task"],"result":("Agent failed: "+type(o).__name__) if isinstance(o,Exception) else o} for t,o in zip(tasks,outcomes)]
        if len(results)==1: answer=results[0]["result"]
        else:
            answer=await self.provider.generate([
            {"role":"system","content":"You are the RemoteAI Coordinator. Synthesize specialist outputs into one coherent response. Remove repetition and disclose failures."},
            {"role":"user","content":json.dumps(results,ensure_ascii=False)}])
        return {"response":answer,"agents":[x["agent"] for x in results],"subtasks":len(tasks)}
