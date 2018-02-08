#!/bin/bash

DST=$1

if [ "${DST}" == "" ]; then
    echo Destination is not specified. Exiting.
    exit 1
fi

TRACE=`traceroute -n -w 1 ${DST} | awk '{if (NR>1) print "HOP_" $1 "=" $2}'`
eval "${TRACE}"
HOPS=`echo "${TRACE}" | wc -l`
for hop in `seq 1 ${HOPS}`; do
     HOP_ID="HOP_${hop}"
     if [ "${!HOP_ID}" != "*" ]; then
         REV_IP=`dig -x ${!HOP_ID} | grep PTR | tail -n 1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
         ASN=`dig ${REV_IP}.origin.asn.cymru.com TXT +short | sed 's/"//g' | awk '{print $1}' | tail -n 1`
         echo "Hop: ${hop} / IP: ${!HOP_ID} / ASN: ${ASN}"
     else
         echo "Hop: ${hop} / IP: * / ASN: NA"
     fi
done
