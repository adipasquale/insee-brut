FUNCTION_NAME=${1:?Specify target lambda function name}
tmpdir=$(mktemp -d /tmp/lambda-XXXXXX)
zipfile=$tmpdir/lambda.zip

mkdir $tmpdir/package
pip3 install -r requirements.txt --target $tmpdir/package
cd $tmpdir/package
zip -r9 $zipfile .
cd -
zip -g $zipfile *.py static_assets/* templates/*

# "aws" command (fixing shabang line)
# rsync -va $virtualenv/bin/aws $tmpdir/aws
# perl -pi -e '$_ ="#!/usr/bin/python\n" if $. == 1' $tmpdir/aws
# (cd $tmpdir; zip -r9 $zipfile aws)

echo "starting to update function on AWS ..."
aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$zipfile
echo "zipfile is $zipfile"
echo "finished !"