from rectpack import newPacker #https://github.com/secnot/rectpack/blob/master/README.md
import  pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def read_fabric_csv(file_path):
    df = pd.read_csv(file_path)
    fabric = df[df['pattern'] == 'fabric'].iloc[0]
    patterns = df[df['pattern'] != 'fabric']
    fabric_width = float(fabric['width'])
    fabric_height = float(fabric['height'])
    pattern_list = []
    for _, row in patterns.iterrows():
        pattern_list.append({
            'name': row['pattern'],
            'width': int(row['width']),
            'height': int(row['height'])
        })
    return fabric_width, fabric_height, pattern_list


#rectangles = [(100, 30), (40, 60), (30, 30),(70, 70), (100, 50), (30, 30)]
#bins = [(300, 450), (80, 40), (200, 150)]
fabric_width, fabric_height, pattern_list = read_fabric_csv('fabric.csv')
patterns_area_sum = lambda patterns: sum(p['width'] * p['height'] for p in patterns)
number_of_bins = math.ceil(patterns_area_sum(pattern_list) / (fabric_width * fabric_height))
#print(f"Number of bins: {number_of_bins}")
def pack_patterns(pattern_list, fabric_width, fabric_height):
    rectangles = [(p['width'], p['height'],p['name']) for p in pattern_list]
    bins = [(fabric_width, fabric_height)] * number_of_bins

    packer = newPacker(rotation=False)

    # Add the rectangles to packing queue
    for r in rectangles:
        packer.add_rect(*r)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)

    # Start packing
    packer.pack()
    # Get the list of rectangles that could not be packed
    all_rects = packer.rect_list()
    unfitted_rects = [rect for rect in all_rects if rect[0] is None]
    return packer, rectangles, bins, all_rects, unfitted_rects

packer, rectangles, bins, all_rects, unfitted_rects = pack_patterns(pattern_list, fabric_width, fabric_height)
for rect in all_rects:
    b, x, y, w, h, rid = rect
    #print(rect)
    
def visualize_packing(packer, fabric_width, fabric_height, output_file='pattern_layout.png', unfitted_rects=None):
    fig, ax = plt.subplots( len(bins),1, figsize=(10 * len(bins), 40))

    # Visualize each bin
    if len(bins) == 1:
        axes = [ax]
    else:
        axes = ax
    
    for i, abin in enumerate(packer):
        axes[i].set_xlim(0, fabric_width)
        axes[i].set_ylim(0, fabric_height)
        axes[i].set_aspect('equal')
        axes[i].set_xlabel('Width')
        axes[i].set_ylabel('Height')
        axes[i].set_title(f'Piece {i+1}')
        axes[i].grid(True, alpha=0.3)
        # Draw bin outline
        axes[i].add_patch(patches.Rectangle((0, 0), fabric_width, fabric_height, edgecolor='black', facecolor='none'))
        # Draw packed rectangles
        for rect in abin:
            x = rect.x
            y = rect.y
            w = rect.width
            h = rect.height
            rect_patch = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='black', facecolor='lightblue', alpha=0.7)
            axes[i].add_patch(rect_patch)
            # Find pattern name by matching width and height
            pattern_name = rect.rid
            axes[i].text(x + w/2, y + h/2, f"{pattern_name}: {w}x{h}", ha='center', va='center', fontsize=10)

        if unfitted_rects:
            # Add an extra subplot for unfitted rectangles
            extra_ax = fig.add_subplot(len(bins)+1, 1, len(bins)+1)
            extra_ax.set_title("Unfitted Rectangles")
            extra_ax.set_xlim(0, fabric_width)
            extra_ax.set_ylim(0, fabric_height)
            extra_ax.set_aspect('equal')
            extra_ax.set_xlabel('Width')
            extra_ax.set_ylabel('Height')
            extra_ax.grid(True, alpha=0.3)
#            extra_ax.add_patch(patches.Rectangle((0, 0), fabric_width, fabric_height, edgecolor='black', facecolor='none'))

            for rect in unfitted_rects:
                _, x, y, w, h, rid = rect
                pattern_name = next((p['name'] for p in pattern_list if p['width'] == w and p['height'] == h), "")
                extra_ax.text(f"{pattern_name}: {w}x{h}", ha='center', va='center', fontsize=10)
    plt.tight_layout()
    

    return fig


# Call the function
if __name__ == "__main__":
    fig = visualize_packing(packer, fabric_width, fabric_height)
    for ax in fig.axes:
        ax.figure.canvas.toolbar_visible = True
        ax.figure.canvas.header_visible = False
        ax.figure.canvas.footer_visible = False
        ax.figure.canvas.scrollable = True
    #plt.tight_layout()
    #plt.savefig('pattern_layout.png', dpi=150, bbox_inches='tight')
    plt.show()