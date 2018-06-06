#!/bin/bash

cd $(dirname $0)
python setup.py sdist | awk 'BEGIN{count=0}/^.*$/{count++; printf("running setup sdist: %d\r", count)}END{printf("\r\n")}'
VERSION=$(ls dist/*.tar.gz | tail -n 1 | sed -ne 's/[^-]*-\(.*\).tar.gz/\1/p')
cp dist/fibra-${VERSION}.tar.gz /tmp/fibra-${VERSION}.orig.tar.gz
( cd /tmp
  rm -fr fibra-${VERSION}/ 2>/dev/null
  tar zxf fibra-${VERSION}.orig.tar.gz 
  cd fibra-${VERSION}/
  dh_make --yes --indep --file ../fibra-${VERSION}.orig.tar.gz )
cp debian/* /tmp/fibra-${VERSION}/debian
( cd /tmp/fibra-${VERSION}/
  find debian -iname "*.ex" -execdir rm {} \; -or -name "*.source" -execdir rm {} \; -or -name "*~" -execdir rm {} \;
  debuild )

echo dput mentors $(ls /tmp/fibra_${VERSION}-*_*.changes | tail -n 1 )
