module switch_plate(rows, cols, ospace=5, ispace=5, plate_d=2) {
    echo(rows=rows,cols=cols,ospace=ospace,ispace=ispace,plate_d=plated);
    // params
    sw_w=14.1;
    sw_h=14.1;
    plate_w=(sw_w*rows + ispace*(rows-1) + ospace*2);
    plate_h=(sw_h*cols + ispace*(cols-1) + ospace*2);

    difference() {
        cube([plate_w, plate_h, plate_d]);
        for (i=[0:(rows-1)]) {
            for (j=[0:(cols-1)]) {
                translate([ospace+i*(sw_w+ispace), ospace+j*(sw_h+ispace), -1]) cube ([sw_w, sw_h, plate_d+2]);
            }
        }
    }
}