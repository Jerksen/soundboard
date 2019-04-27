include <rcube.scad>
thickness=2;
pi_size = [85+27.5,56+27.5,50];
pi_h1=[7, 7, 0];
pi_hole_offset=[58, 49, 0];
pi_holes_r=2.5/2;
peg_height=5;
corner_r = [3,3,3,3];

module case()
{
    union(){
        difference() {
            rcube(pi_size, corner_r);
            translate([1, 1, 2]) rcube(pi_size-[2,2,1], corner_r);
        }
    }
}

module case_w_holes() {
    difference() {
        case();
        // power hole
        side_hole(20,10,[50,0,0],[2,2,2,2]);
        
        // audio jack
        
        // cable outs
    }
    
}

module top_plate(size, z_level) {
    echo(size=size, z_level=z_level);
}

module mounting_peg(h, r1, r2) {
    echo(h=h,r1=r1,r2=r2);
    difference() {
        cylinder(h, r=r2);
        translate([0,0,-1]) cylinder(h+2, r=r1);
    }
}

module side_hole(h,w,pos,r) {
    echo(h=h, w=w, pos=pos, r=r);
    if (pos.x == 0) {
        translate([pos.x-1, pos.y, thickness]) rotate([0,90,180]) rcube([h,w,thickness+2],r);
        }
    else {
        translate([pos.x, pos.y-1, thickness]) rotate([90,0,180]) rcube([h,w,thickness+2],r);
    }
}

union() {
    case_w_holes();
    for (i = [0:1]) {
        for (j = [0:1]) {
            translate([pi_h1[0] + (i*pi_hole_offset[0]), pi_h1[1] + (j*pi_hole_offset[1]), 0]) mounting_peg(peg_height, pi_holes_r, pi_holes_r+1);
        }
    }
}