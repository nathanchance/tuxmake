# Runtimes

By default, tuxmake will use any toolchains that you have installed on your
system. i.e., if you specify `--toolchain` and `--target-arch`, the appropriate
(cross) compilers must be available locally in your `$PATH`.

Alternatively, tuxmake supports the concept of runtimes. You can think of
runtimes as both an underlying backend to run the actual build commands, as
well as a provider of toolchains. For example, the `docker` runtime will run
your builds in docker containers, using toolchain container images provided by
the tuxmake maintainers. When running a build, the tuxmake docker runtime will
download the container image that provides the selected (cross) toolchain to
build for the selected target architecture.

The following runtimes are available:

* `null`: the default runtime. Assumes you have any necessary toolchain
  installed on your system.
* `docker`: the docker runtime. Runs builds in docker containers, using images
  provided by the tuxmake maintainers (or the image informed via
  **-i/--docker-image**). Will hit the network every time, looking for updated
  images.
* `docker-local`: the same as `docker`, but will only use images that you
  already have locally.
