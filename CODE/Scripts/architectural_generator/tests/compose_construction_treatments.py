"""Compose construction benchmark sheets from the captured frames."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / 'evidence' / 'construction_treatments'


def main():
    labels = [('normal','clay'), ('normal','material'), ('close','clay'), ('close','material')]
    font = ImageFont.load_default(size=19)
    for name, title in (('smithy','Lowmark Smithy'), ('gatehouse','Thornfell Gatehouse')):
        width, height, label_height = 800, 550, 34
        sheet = Image.new('RGB',(width*2,(height+label_height)*len(labels)),(32,36,40))
        draw = ImageDraw.Draw(sheet)
        for row,(distance,finish) in enumerate(labels):
            for col,variant in enumerate(('before','after')):
                x,y = col*width,row*(height+label_height)
                with Image.open(ROOT/variant/name/f'{distance}_{finish}_0.png') as source:
                    image = source.convert('RGB')
                image.thumbnail((width,height),Image.Resampling.LANCZOS)
                draw.text((x+12,y+6),f'{title} | {variant.title()} | {distance.title()} {finish}',
                          fill='white',font=font)
                sheet.paste(image,(x,y+label_height))
        sheet.save(ROOT/f'{name}_review.jpg',quality=92,optimize=True)


if __name__=='__main__':
    main()
