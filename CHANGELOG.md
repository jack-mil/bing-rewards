# Changelog

## [3.3.1](https://github.com/jack-mil/bing-rewards/compare/v3.3.0...v3.3.1) (2026-02-06)


### Build System

* **deps:** bump actions/checkout from 4 to 5 ([#99](https://github.com/jack-mil/bing-rewards/issues/99)) ([4bec9b5](https://github.com/jack-mil/bing-rewards/commit/4bec9b5346cb81c9955d2790f1420ad479c7f27a))
* **deps:** bump allowed version of uv_build and python (3.15) ([9a760f0](https://github.com/jack-mil/bing-rewards/commit/9a760f0520de13d4a16bc329eb37b6467ee9c7bd))
* **deps:** bump astral-sh/setup-uv from 6 to 7 ([34b1340](https://github.com/jack-mil/bing-rewards/commit/34b1340e73d8c3591e0da6a5d4d1104ab39b4955))
* **deps:** Update development dependencies in uv.lock ([a3b4861](https://github.com/jack-mil/bing-rewards/commit/a3b4861a386c2ce96402cf98bf07663c24e967ce))
* pin uv_build to version 0.9 ([40a7d6b](https://github.com/jack-mil/bing-rewards/commit/40a7d6b371421cbcc4d79408502765e6c455c84c))


### Continuous Integration

* bump actions/setup-python from 5 to 6 ([#101](https://github.com/jack-mil/bing-rewards/issues/101)) ([222efe8](https://github.com/jack-mil/bing-rewards/commit/222efe8a1577a475e2926b9a68418b7d1a6fe679))
* Update workflow actions ([81067c6](https://github.com/jack-mil/bing-rewards/commit/81067c6923c8e1d48f1c479b0ef158c9e3351461))

## [3.3.0](https://github.com/jack-mil/bing-rewards/compare/v3.2.1...v3.3.0) (2025-07-17)


### Features

* add a very slight delay between keystrokes for more reliable text input ([#86](https://github.com/jack-mil/bing-rewards/issues/86)) ([b3cd58d](https://github.com/jack-mil/bing-rewards/commit/b3cd58d58aa50084b7baace10120e494af0772dc))
* add cli arguments to override options from config file (e.g. --no-window) ([#94](https://github.com/jack-mil/bing-rewards/issues/94)) ([08874ff](https://github.com/jack-mil/bing-rewards/commit/08874ff708ab99af83ff3f4278767cecf4418f59))
* enable color argparse help on python &gt;= 3.14 ([98ad897](https://github.com/jack-mil/bing-rewards/commit/98ad897e4d3121d0fe1b3fb306f453de68a2afdf))
* more configuration can be set in the config file ([#94](https://github.com/jack-mil/bing-rewards/issues/94)) ([08874ff](https://github.com/jack-mil/bing-rewards/commit/08874ff708ab99af83ff3f4278767cecf4418f59))


### Bug Fixes

* absolute path to script in help output on python &gt;= 3.14 ([98ad897](https://github.com/jack-mil/bing-rewards/commit/98ad897e4d3121d0fe1b3fb306f453de68a2afdf))


### Build System

* switch to the new uv_build backend for wheels and sdist ([35b6bd7](https://github.com/jack-mil/bing-rewards/commit/35b6bd7905acd5f81b6a8fe5a62e225279d2ee82))

## [3.2.1](https://github.com/jack-mil/bing-rewards/compare/v3.2.0...v3.2.1) (2025-06-20)


### Changes

* removed some potentially objectionable random search terms ([#87](https://github.com/jack-mil/bing-rewards/issues/87)) ([2f08693](https://github.com/jack-mil/bing-rewards/commit/2f08693666c1b6d4ca5e5dcfa064c7a8d8278cb8))

## [3.2.0](https://github.com/jack-mil/bing-rewards/compare/v3.1.0...v3.2.0) (2025-06-01)


### Features

* enhance browser subprocess termination ([#61](https://github.com/jack-mil/bing-rewards/issues/61)) ([d902ecd](https://github.com/jack-mil/bing-rewards/commit/d902ecd81b68d47e8000ad814b56b5929fe771b0))
* search-delay option can specify a random range to delay ([#63](https://github.com/jack-mil/bing-rewards/issues/63)) ([fc82c11](https://github.com/jack-mil/bing-rewards/commit/fc82c1116f58dc372994bba52eea93546ac6aa88))
* skip verifying browser path when --no-window flag is used ([8e98011](https://github.com/jack-mil/bing-rewards/commit/8e9801102b484442e247435bf8b5e36c1096ed30))
* support and test on Python 3.14 ([b018261](https://github.com/jack-mil/bing-rewards/commit/b018261690fe6ec41f9957e8835f8a9410024373))


### Bug Fixes

* **ci:** remove $schema from release-please-manifest ([f3decf5](https://github.com/jack-mil/bing-rewards/commit/f3decf5f051b570bde3de1fde80d315fc2c34027))


### Documentation

* add UV to install instructions ([64ec334](https://github.com/jack-mil/bing-rewards/commit/64ec33447c34733505fcb1418c0e2700fdcc046f))


### Build System

* ditch dynamic vcs versioning ([6a4af97](https://github.com/jack-mil/bing-rewards/commit/6a4af97cfabca11c6c34696f74a09606dfe38736))
* make releaseplease also bump version in uv.lock ([008a9e2](https://github.com/jack-mil/bing-rewards/commit/008a9e2b3522eb572504ee72526b6ab9f65229bd))
* use UV for project & dep management ([9d65882](https://github.com/jack-mil/bing-rewards/commit/9d658825c4c4fe617b8d224221cbbfc24a4515ec))


### Continuous Integration

* add release-please workflow ([2fe5143](https://github.com/jack-mil/bing-rewards/commit/2fe514376fab3dbfa34ce4cafc049955320b5f67))
* Use the ruff action for linting ([e288ec7](https://github.com/jack-mil/bing-rewards/commit/e288ec75df2290e206b97b379153b79c25da99ae))
