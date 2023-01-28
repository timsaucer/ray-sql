import ray
from raysql import Context

@ray.remote
class Worker:
    def __init__(self):
        self.ctx = Context()

    def execute_query_partition(self, plan_bytes, part):
        plan = self.ctx.deserialize_execution_plan(plan_bytes)
        print("Executing partition #{}:\n{}".format(part, plan.display_indent()))

        # This is delegating to DataFusion for execution, but this would be a good place
        # to plug in other execution engines by translating the plan into another engine's plan
        # (perhaps via Substrait, once DataFusion supports converting a physical plan to Substrait)
        self.ctx.execute_partition(plan, part)

        return True


