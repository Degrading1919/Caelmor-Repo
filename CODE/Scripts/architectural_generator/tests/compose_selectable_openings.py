"""Compose review sheets from the native selectable-openings fixture."""
import compose_construction_library as layout


def main():
    layout.ROOT = layout.EVIDENCE/'selectable_openings'
    layout.ROOT.mkdir(exist_ok=True)
    frames = layout.EVIDENCE.parent/'dist'/'component_verification'
    layout.sheet('window_fit.jpg',('Previous ordinary window','Seated panes and sash','Narrow guided window'),
                 [(view.title(),[frames/f'{state}_{view}.png' for state in
                               ('legacy_window','new_unmoved_window','guided_window')])
                  for view in ('front','oblique','rear')],width=650)
    layout.sheet('opening_move.jpg',('Before placement edit','Ordinary window moved 0.50 m'),
                 [(view.title(),[frames/f'{state}_{view}.png' for state in ('before_move','after_move')])
                  for view in ('elevation','gameplay')],width=800)
    layout.sheet('mapped_finishes.jpg',('Production clay','Assigned PBR'),
                 [(view.title(),[frames/f'{state}_{view}.png' for state in ('after_move','mapped_pbr')])
                  for view in ('elevation','gameplay')],width=800)


if __name__=='__main__':
    main()
