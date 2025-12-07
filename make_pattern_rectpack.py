from rectpack import newPacker #https://github.com/secnot/rectpack/blob/master/README.md
import  pandas as pd
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

def pack_patterns(pattern_list, fabric_width, fabric_height):
    rectangles = [(p['width'], p['height']) for p in pattern_list]
    bins = [(fabric_width, fabric_height)]

    packer = newPacker(rotation=False)

    # Add the rectangles to packing queue
    for r in rectangles:
        packer.add_rect(*r)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)

    # Start packing
    packer.pack()
    # Full rectangle list
    all_rects = packer.rect_list()
    return packer, rectangles, bins, all_rects

packer, rectangles, bins, all_rects = pack_patterns(pattern_list, fabric_width, fabric_height)
for rect in all_rects:
    b, x, y, w, h, rid = rect
    print(rect)
    
def visualize_packing(packer, fabric_width, fabric_height, output_file='pattern_layout.png'):
    fig, ax = plt.subplots(1, len(bins), figsize=(6 * len(bins), 6))

    # Use ax[i] for each bin
    # Set axis limits and labels
    ax.set_xlim(0, fabric_width)
    ax.set_ylim(0, fabric_height)
    ax.set_aspect('equal')
    ax.set_xlabel('Width')
    ax.set_ylabel('Height')
    ax.set_title('Pattern Layout')
    ax.grid(True, alpha=0.3)    
    # Draw bins and packed rectangles
    for abin in packer:
         ax.add_patch(patches.Rectangle((0, 0), fabric_width, fabric_height, edgecolor='black', facecolor='none'))
         for rect in abin:
            # rect is a Rectangle object
            x = rect.x # rectangle bottom-left x coordinate
            y = rect.y # rectangle bottom-left y coordinate
            w = rect.width
            h = rect.height
            b=abin
            rid=rect.rid # rectangle id
            # Draw rectangle
            rect_patch = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='black', facecolor='lightblue', alpha=0.7)
            ax.add_patch(rect_patch)
 
            # Add text label
            ax.text(x + w/2, y + h/2, f"{w}x{h}", ha='center', va='center', fontsize=10)
    

    return fig


# Call the function
if __name__ == "__main__":
    fig = visualize_packing(packer, fabric_width, fabric_height)
    plt.tight_layout()
    plt.savefig('pattern_layout.png', dpi=150, bbox_inches='tight')
    plt.show()