# Makefile for source rpm: ksh
# $Id$
NAME := ksh
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
