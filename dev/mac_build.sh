cd ../lib/
rm -rf mdi_build
mkdir mdi_build
cd mdi_build
cmake -Dlanguage=Python ../mdi
make
