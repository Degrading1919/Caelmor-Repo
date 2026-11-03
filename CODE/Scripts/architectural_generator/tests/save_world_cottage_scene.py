"""Save the four-region neutral-clay editable scene and paired hash manifest."""
import importlib.util
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("world_evidence_renderer",ROOT/"tests"/"render_world_evidence.py")
render=importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)
from caelmor_architecture.model import Settings

settings=[Settings(seed=91,function="COTTAGE",region=region,wealth="MODEST",
    detail="LOW",use_grammar=True,world_aware=True)
    for region in ("LOWMARK","THORNFELL","MIRE","EMBERHOLT")]
render.OUT.mkdir(parents=True,exist_ok=True)
render._save_editable_cottage_scene(settings)
print("Saved four-region editable cottage scene with engine/backend hash agreement.")
