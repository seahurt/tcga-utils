#!perl
use warnings;
use strict;

die("Usage:perl $0 <input.bed> <output.bed> \n") if @ARGV<2;

my($input,$output)=@ARGV;

open DUP,"$input";
open DIST, ">$output";

my $key='null';
my @value;
while(<DUP>){
    if (/^#/){
        print DIST;
        next;
    }
    chomp;
    my($chr,$start,$end,@info)=split;
    my $infostr=join '.',@info;
    # if exist dup pos, judge the infostr,if infostr exists, next
    # if infostr not exists, print,and add the info to value array
    if ($key eq "$chr+$start+$end"){
        if (grep /$infostr/, @value){
            next;
        }else{
            print DIST ",$infostr";
            push @value, $infostr;
        }
    }
    # if not exist the key, print out the whole line 
    else{
        $key="$chr+$start+$end";
        undef @value;
        push @value, $infostr;
        print DIST "\n$chr\t$start\t$end\t$infostr";
    }
}
close DUP;
close DIST;
   
