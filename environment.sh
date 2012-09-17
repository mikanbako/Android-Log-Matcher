# Set environment to develop.
#
# Execute source command with this script at its same directory.

TOP_DIRECTORY=`pwd`

export PYTHONPATH="$TOP_DIRECTORY/src/main":"$TOP_DIRECTORY/src/test":"$TOP_DIRECTORY/externals/test"
