dev = true;
if (dev) {
    $fa=1;
    $fs=1.5;
} else {
    $fa=1;
    $fs=0.5;
}

include <plate.scad>;

//setup vars
plate_z = 1.5;
pi_x = 100;
pi_y = 100;
pi_z = 20;


//make the plate
switch_plate(1,2, plate_d=plate_z);

// rim the plate with a way to attach it to the case

// make the bottom of the case