#!/usr/bin/perl
#
# This code was derived from Chris Meyers' script described here --
# http://chrismeyers.org/2012/06/02/raspberry-pi-no-hdmi-cable-or-no-hdmi-display-blink-ip-address-to-ok-led/
# -- and available here -- https://gist.github.com/chrismeyersfsu/2858824

my $dev = "/sys/class/leds/led0/brightness";
my $OFF = "1";
my $ON = "0";

my ($ip) = `ifconfig`=~/ddr:(.*?) /;
print "$ip\n";

# Strip out the .'s
$ip =~ s/\.//g;
print "$ip\n";

exit;

while (1) {
    display_start();

    while ($ip =~ /(.)/g) {
        my $char = $1;
        print "$char\n";
        if ($char eq '0' || $char == 0) {
	    display_zero();
        } else {
            display_blink($char, .25, .25);
        }
        usleep(2);
    }
    usleep(2);
}

sub display_start {
    for (my $i=0; $i < 50; $i++) {
        usleep(.05);
        outb($ON);
        usleep(.05);
        outb($OFF);
    }
    usleep(4);
}

sub display_zero {
    for (my $i=0; $i < 10; $i++) {
        usleep(.05);
        outb($ON);
        usleep(.05);
        outb($OFF);
    }
}

sub display_blink {
    my $char = shift;
    my $dwell = shift;
    my $delay = shift;

    for (my $i=0; $i < $char; $i++) {
        usleep($dwell);
	outb($ON);
        usleep($delay);
	outb($OFF);
    }
}

sub outb {
    my $char = shift;
    `echo $char > $dev`;
}

sub usleep {
    my $time_seconds = shift;
    select(undef, undef, undef, $time_seconds);
}
