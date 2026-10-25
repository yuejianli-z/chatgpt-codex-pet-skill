"""Create original geometric test pixels, not a pet or production example."""
from pathlib import Path
import argparse,json,hashlib
from PIL import Image,ImageDraw

def create_fixture(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    frames=[]
    for x in [12,24,36]:
        im=Image.new('RGB',(64,64),'white');ImageDraw.Draw(im).rectangle((x,24,x+10,34),fill='#286a91');frames.append(im)
    path=directory/'geometry-test.gif'
    if path.exists():raise FileExistsError('Refusing to overwrite existing fixture; choose a fresh directory')
    holds=[100,200,300];frames[0].save(path,save_all=True,append_images=frames[1:],duration=holds,loop=0)
    with Image.open(path) as check:
        actual=[]
        for i in range(check.n_frames):check.seek(i);check.load();actual.append(check.info['duration'])
    assert actual==holds
    result={'purpose':'original geometry for encoder tests; NOT character animation or visual-quality evidence','license':'MIT, same as this fixture generator','frames':3,'duration_ms':600,'decoded_holds_ms':actual,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (directory/'fixture-check.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output_dir',type=Path);a=p.parse_args();print(json.dumps(create_fixture(a.output_dir),indent=2))
