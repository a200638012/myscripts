1. modify your svn config in your home dir like ~/.subversion/config
   1. uncomment diff-cmd
   2. diff-cmd = /yourpath_to_svn_bcompare_wrapper.sh
2. chomd +x /yourpath_to_svn_bcompare_wrapper.sh
3. now you can use svn diff xxx.file by bcompare