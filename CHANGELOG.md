# Changelog

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
