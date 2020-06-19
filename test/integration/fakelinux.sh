setUp() {
  tmpdir=$(mktemp --directory --tmpdir tuxmake-integration-tests-XXXXXXXXXX)
  export XDG_CACHE_HOME="${tmpdir}/cache"
  cp -r test/fakelinux/ "${tmpdir}/linux"
  cd "${tmpdir}/linux"
}

tearDown() {
  cd - >/dev/null
  rm -rf "${tmpdir}"
}

failrun() {
  export FAIL="$1"
  shift
  run "$@"
  unset FAIL
}

run() {
  echo '    $' "$@"
  rc=0
  "$@" > stdout 2> stderr || rc=$?
  cat stdout stderr | sed -e 's/^/    /'
  export rc
}

test_basic() {
  run tuxmake
  assertEquals 0 "$rc"
  assertTrue 'config: PASS' "grep 'config: PASS' stderr"
  assertTrue 'kernel: PASS' "grep 'kernel: PASS' stderr"
  assertFalse 'no ARCH=' 'grep ARCH= stdout'
  assertFalse 'no CROSS_COMPILE=' 'grep CROSS_COMPILE= stdout'
  assertFalse 'no CC=' 'grep CC= stdout'
}

test_cross() {
  run tuxmake --target-arch=arm64
  assertEquals 0 "$rc"
  assertTrue 'ARCH=' "grep 'ARCH=arm64' stdout"
  assertTrue 'CROSS_COMPILE=' "grep 'CROSS_COMPILE=aarch64-linux-gnu-' stdout"
  assertFalse 'no CC=' 'grep CC= stdout'
  assertTrue 'Image.gz' 'test -f $XDG_CACHE_HOME/tuxmake/builds/1/Image.gz'
}

test_toolchain() {
  run tuxmake --toolchain=gcc-10
  assertEquals 0 "$rc"
  assertFalse 'no ARCH=' 'grep ARCH= stdout'
  assertFalse 'no CROSS_COMPILE=' 'grep CROSS_COMPILE= stdout'
  assertTrue 'CC=' "grep 'CC=gcc-10' stdout"
}

test_cross_toolchain() {
  run tuxmake --target-arch=arm64 --toolchain=gcc-10
  assertEquals 0 "$rc"
  assertTrue 'ARCH=' "grep 'ARCH=arm64' stdout"
  assertTrue 'CROSS_COMPILE=' "grep 'CROSS_COMPILE=aarch64-linux-gnu-' stdout"
  assertTrue 'CC=' "grep 'CC=aarch64-linux-gnu-gcc-10' stdout"
  assertTrue 'Image.gz' 'test -f $XDG_CACHE_HOME/tuxmake/builds/1/Image.gz'
}

test_fail() {
  failrun kernel tuxmake
  assertEquals 2 "$rc"
  assertTrue 'grep "config: PASS" stderr'
  assertTrue 'grep "kernel: FAIL" stderr'
}

. shunit2
