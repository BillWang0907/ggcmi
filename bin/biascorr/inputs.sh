#!/bin/bash

root=/project/ggcmi

# Header
echo indir reffile agglvl outdir

# gadm0
echo $root/AgMIP.output/processed/aggs/gadm0 $root/AgMIP.input/other.inputs/reference/faostat/faostat.1961-2012.gadm0.nc4 gadm0 $root/AgMIP.output/processed/biascorr/gadm0/faostat

# fpu
echo $root/AgMIP.output/processed/aggs/fpu $root/AgMIP.input/other.inputs/reference/ray/ray.1961-2008.fpu.nc4 fpu $root/AgMIP.output/processed/biascorr/fpu/ray
echo $root/AgMIP.output/processed/aggs/fpu $root/AgMIP.input/other.inputs/reference/iizumi/iizumi.1982-2006.fpu.nc4 fpu $root/AgMIP.output/processed/biascorr/fpu/iizumi

# kg
echo $root/AgMIP.output/processed/aggs/kg $root/AgMIP.input/other.inputs/reference/ray/ray.1961-2008.kg.nc4 kg $root/AgMIP.output/processed/biascorr/kg/ray
echo $root/AgMIP.output/processed/aggs/kg $root/AgMIP.input/other.inputs/reference/iizumi/iizumi.1982-2006.kg.nc4 kg $root/AgMIP.output/processed/biascorr/kg/iizumi

# global
echo $root/AgMIP.output/processed/aggs/global $root/AgMIP.input/other.inputs/reference/faostat/faostat.1961-2012.global.nc4 global $root/AgMIP.output/processed/biascorr/global/faostat
