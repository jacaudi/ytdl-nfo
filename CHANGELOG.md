# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v0.1.0](https://github.com/jacaudi/ytdl-nfo/releases/tag/v0.1.0) - 2025-11-30

- [`5d6396e`](https://github.com/jacaudi/ytdl-nfo/commit/5d6396eb7a679feb19d2dd7ff28c0c7239413b1e) feat: add automated package releases with Uplift and GitHub Actions (#9)
- [`2fe1418`](https://github.com/jacaudi/ytdl-nfo/commit/2fe141815cad41034eaa91949f464e923119a71e) feat: add JSON reporting to CI workflow (#7)
- [`064f4d1`](https://github.com/jacaudi/ytdl-nfo/commit/064f4d1541f0c75925dcc4eb1070fff4a9440394) feat: add semgrep security scanning to CI
- [`e8df2ee`](https://github.com/jacaudi/ytdl-nfo/commit/e8df2eeea548f860bd054d23aefd43ca1a8855af) feat: add semgrep security scanning to CI
- [`ad64a27`](https://github.com/jacaudi/ytdl-nfo/commit/ad64a274c786f1e8b19bd8be974883cf53eea679) fix: install dev dependencies in CI workflow
- [`936e98f`](https://github.com/jacaudi/ytdl-nfo/commit/936e98ffe8337675942b0155af31739d644ba8b9) feat: add GitHub Actions workflow for release management
- [`b897f9d`](https://github.com/jacaudi/ytdl-nfo/commit/b897f9d0382105984b3f3d6f43931d8ccb153f6f) refactor: migrate from pkg_resources to importlib.resources
- [`de8d518`](https://github.com/jacaudi/ytdl-nfo/commit/de8d51828691434a7ce901a74157e9ec7d5dada8) fix: update directory name for action workflows
- [`967be59`](https://github.com/jacaudi/ytdl-nfo/commit/967be597972b765e2dec64b60c3d992914c709f8) feat: add renovate workflow and config
- [`6321e90`](https://github.com/jacaudi/ytdl-nfo/commit/6321e9070b8c3148e556eb6b781b142a46ab912e) Add design document for uv migration and test suite
- [`41aaf2d`](https://github.com/jacaudi/ytdl-nfo/commit/41aaf2decfcbe9b8faa02967dfe905cfbc75f66a) feat: migrate to uv and add test suite (#1)
- [`459d218`](https://github.com/jacaudi/ytdl-nfo/commit/459d218ffe2cc9c90e4c74236e054263bfa09de9) Add nix dev environment, update to poetry 2.0.0 specification, bump pyyaml>=6.0.1
- [`e1fac6e`](https://github.com/jacaudi/ytdl-nfo/commit/e1fac6ef27cc0210db62bbb694edd913eb2f486d) Merge pull request #38 from breakid/documentation
- [`3d5409d`](https://github.com/jacaudi/ytdl-nfo/commit/3d5409d24514ee73fc8384e78fb2023f834f87e9) Merge pull request #37 from breakid/nebula
- [`006e90c`](https://github.com/jacaudi/ytdl-nfo/commit/006e90c2ebf8008834eebfa94ddf6fb97ace857b) Remove obsolete 'python.linting' VSCode settings
- [`04a2aa5`](https://github.com/jacaudi/ytdl-nfo/commit/04a2aa5f5283350a7dfb7e57834de098d6483412) Merge branch 'documentation' of github.com:breakid/ytdl-nfo into documentation
- [`fb0edb8`](https://github.com/jacaudi/ytdl-nfo/commit/fb0edb8a8b3a7e658ea2a1a9ab381024efcf7033) Edited and formatted README.md
- [`75c7733`](https://github.com/jacaudi/ytdl-nfo/commit/75c77339988dab961fdc0d08854d787e5bd387a7) Edited and formatted ReADME.md
- [`2b2de1a`](https://github.com/jacaudi/ytdl-nfo/commit/2b2de1ac89aadffd69ab04c6620c1ddb44329848) Add Nebula extractor configs
- [`c034144`](https://github.com/jacaudi/ytdl-nfo/commit/c0341448dcd84fc7359aab5dd252e5fc962dad6c) Merge pull request #36 from owdevel/support-limited-nested-tags-#29
- [`dc43864`](https://github.com/jacaudi/ytdl-nfo/commit/dc4386454bb78df36049d507a935341ab522a72a) Prevent deliminator usage when not using lists
- [`6bb2d37`](https://github.com/jacaudi/ytdl-nfo/commit/6bb2d37eb5c05fe23c7c0230520e1a3c5e7a1330) Add support for nested tags with >
- [`c0eacd9`](https://github.com/jacaudi/ytdl-nfo/commit/c0eacd9aa458cb250290c05517fcda89701f1c4b) Merge pull request #35 from pineapplemachine/extractor-config-twitch-vod
- [`79a05d9`](https://github.com/jacaudi/ytdl-nfo/commit/79a05d9a8460a2f21026e813fe1220e5c2c39abc) Merge pull request #34 from pineapplemachine/fix-issue-32
- [`5d6f218`](https://github.com/jacaudi/ytdl-nfo/commit/5d6f218425e7139badae9d7c6cb0647da2fea829) Merge pull request #31 from pineapplemachine/fix-poetry-2024-07-08
- [`dc4f70c`](https://github.com/jacaudi/ytdl-nfo/commit/dc4f70c84c63a810b0b5eeb2eecb35b14f4a1a6a) Don't abort with KeyError when info json is missing a key
- [`58b32ce`](https://github.com/jacaudi/ytdl-nfo/commit/58b32ce1a8cde2951fd86057fa12738bcde8a627) Also add twitch:clips extractor config
- [`865bec9`](https://github.com/jacaudi/ytdl-nfo/commit/865bec9b181a74a4576dac572bd879e5568cc450) Add twitch:vod extractor + better youtube:tab (playlist) extractor
- [`816e3eb`](https://github.com/jacaudi/ytdl-nfo/commit/816e3eb127c6fc88729fde65f1d0779dc83bac2d) Small unrelated fix to stop polluting my log with JSON parse errors
- [`5180794`](https://github.com/jacaudi/ytdl-nfo/commit/5180794ea89a2c318521755919aee4db310c8dfe) Fix behavior of -w overwrite flag to always use correct nfo path
- [`0bbcc26`](https://github.com/jacaudi/ytdl-nfo/commit/0bbcc2642908868fed576e442ea2723a15f3a43f) Merge branch 'dev' into fix-poetry-2024-07-08
- [`e15ed0c`](https://github.com/jacaudi/ytdl-nfo/commit/e15ed0ce9dbd08fea4fd883a86e14e22a2680c5f) Add setuptools explicitly to poetry dependencies
- [`f62f73e`](https://github.com/jacaudi/ytdl-nfo/commit/f62f73e790b36e4a82f016d798834c1ba70d91ac) Bump version to 0.3.0
- [`5099bc4`](https://github.com/jacaudi/ytdl-nfo/commit/5099bc418341b73383deec09edb7009af07b55f4) Merge pull request #23 from lyarenei/add-zype-extractor
- [`f97cb24`](https://github.com/jacaudi/ytdl-nfo/commit/f97cb24ed3de1092abe1e58318f95aedc140c814) Merge pull request #24 from CorrectRoadH/dev
- [`56eed6e`](https://github.com/jacaudi/ytdl-nfo/commit/56eed6eb24ae9bf6e7c86795327f56d6d4c209f1) Merge pull request #28 from pineapplemachine/extractor-config-vimeo
- [`529824e`](https://github.com/jacaudi/ytdl-nfo/commit/529824e889afe0344764d27d6334483648cc5df9) Merge pull request #27 from pineapplemachine/fixes-2023-08-25
- [`c5a0fdf`](https://github.com/jacaudi/ytdl-nfo/commit/c5a0fdf3b79652e6a8b780dd07f49ccb53766fbb) Add vimeo extractor config yaml
- [`a73c120`](https://github.com/jacaudi/ytdl-nfo/commit/a73c1204a10d1e4b0c2bcd4b143627f22c626ada) Improve handling for an invalid extractor value
- [`07efc54`](https://github.com/jacaudi/ytdl-nfo/commit/07efc54840da1b37925698b095aeaf064386bab9) Add new fallback value for Ytdl_nfo filename attribute
- [`220da35`](https://github.com/jacaudi/ytdl-nfo/commit/220da3584147f2ab0bc3256cfd4c7b50e6f9fdc9) Add "Error" text to missing extractor config message
- [`57dc82b`](https://github.com/jacaudi/ytdl-nfo/commit/57dc82b56f1f1d29dea9b9ff3ed8aed22d8028ef) Fix issues 25 and 26, add vimeo extractor config
- [`0043d1b`](https://github.com/jacaudi/ytdl-nfo/commit/0043d1b9df680b46e234cbc40d5bee6923062d6a) feat: support bilibili nfo
- [`992bdaa`](https://github.com/jacaudi/ytdl-nfo/commit/992bdaab49ef4ed8ac254782a074a6aaa8434bad) Move config to correct place
- [`bcfafeb`](https://github.com/jacaudi/ytdl-nfo/commit/bcfafeb383b0ffe8d0abd71bfa6758e48be8c7d8) Add config for zype extractor
- [`3550bbb`](https://github.com/jacaudi/ytdl-nfo/commit/3550bbb68e46ca2c95f3599c972ac12fbcd86fc3) Removed _type check due for youtube-dl compatability
- [`4376ac1`](https://github.com/jacaudi/ytdl-nfo/commit/4376ac16350e8fff92946026c11b3b846c2392d9) Bump pyproject.toml to v0.2.3 (#15)
- [`d8bb292`](https://github.com/jacaudi/ytdl-nfo/commit/d8bb2923e6865fd816e3c45c66bcefdb187f664e) Bump pyproject.toml to v0.2.3 (#15)
- [`e390d87`](https://github.com/jacaudi/ytdl-nfo/commit/e390d8712f6039f00b72826f43505c5fdb2a2230) Merge pull request #14 from owdevel/dev
- [`87ce20f`](https://github.com/jacaudi/ytdl-nfo/commit/87ce20fbeb56cc1fea82c5fe1fc46416a36ff96c) Merge pull request #12 from owdevel/11-filter-video-types
- [`fe071da`](https://github.com/jacaudi/ytdl-nfo/commit/fe071daeb06e84842632a0fbc99e68802358db48) Added catch to skip non-video nfo files
- [`c95b2ea`](https://github.com/jacaudi/ytdl-nfo/commit/c95b2ea27cdbe640d3fc761fe7b5a0c9cce137b3) Merge pull request #13 from owdevel/Bugfixes
- [`07dcd42`](https://github.com/jacaudi/ytdl-nfo/commit/07dcd4233be9b648dfba1c64c1f4c6a67351f875) Fixed regex multi-search bug and nfo name write bug
- [`a55e177`](https://github.com/jacaudi/ytdl-nfo/commit/a55e17700ae5d16f8a3b5a9f628ef8b3c9ad7bf5) Merge pull request #8 from owdevel/dev
- [`f3e8b4e`](https://github.com/jacaudi/ytdl-nfo/commit/f3e8b4e588c83384c00f3d37006bf31dc2a45d97) Updated README
- [`c8b035f`](https://github.com/jacaudi/ytdl-nfo/commit/c8b035f1db05ce0adb48089a3466307c54b1255d) Added README to build for PyPI
- [`74cb878`](https://github.com/jacaudi/ytdl-nfo/commit/74cb8781af5f9b4cada256c13b5202e7ca8d09c8) Bump version to 0.2.0
- [`d712aec`](https://github.com/jacaudi/ytdl-nfo/commit/d712aec6ff33d71db8d0b1bef22912f2095f3bac) Migrated build system to poetry
- [`a6b4d76`](https://github.com/jacaudi/ytdl-nfo/commit/a6b4d765c85014bcdead728acb4d5c0d4aa75441) Regex incorporation into path walking code
- [`8ef7a2d`](https://github.com/jacaudi/ytdl-nfo/commit/8ef7a2dc17010719d114150a9ec9383ecc6b48f7) Broke out write to a separate function, added custom regex for file matching
- [`de155de`](https://github.com/jacaudi/ytdl-nfo/commit/de155dec54e912b3f5bc60eaf4963e6665281720) Merge pull request #6 from pineapplemachine/fixes-2022-08-06
- [`087e8bb`](https://github.com/jacaudi/ytdl-nfo/commit/087e8bb1c16881a3a619940ac26c551a25a98c56) Unicode & yt-dlp related fixes
- [`7beca9f`](https://github.com/jacaudi/ytdl-nfo/commit/7beca9f17dcdf8f1382a43cf8f9268905338f89b) Merge pull request #5 from owdevel/readme_update
- [`e140242`](https://github.com/jacaudi/ytdl-nfo/commit/e1402429800c0f7b7ef1edc80cd1c8aac15fb277) Updated README for manual installation methods, small grammar tweaks
- [`37c767d`](https://github.com/jacaudi/ytdl-nfo/commit/37c767d2fb9cb6149e707d328795ad49b59ac1d4) Merge pull request #4 from pineapplemachine/master
- [`ffd7370`](https://github.com/jacaudi/ytdl-nfo/commit/ffd73700fb834218358432291314e916f01d20d6) Recognize "--overwrite" flag in CLI args
- [`d253efa`](https://github.com/jacaudi/ytdl-nfo/commit/d253efa00f52813521b4bdc70c810eb8dad22777) Various small improvements to script behavior
- [`fad414b`](https://github.com/jacaudi/ytdl-nfo/commit/fad414bd465aabb93efa4d14d1416a2dac39727a) Added get_nfo
- [`7702fbd`](https://github.com/jacaudi/ytdl-nfo/commit/7702fbd88012db9ce284eeed052d10bef25c5304) Added custom extractor to single file extraction
- [`6ca4ec1`](https://github.com/jacaudi/ytdl-nfo/commit/6ca4ec1b1e6f69feb7c1d10d1df0019b5e60445b) Updated README
- [`144f5e1`](https://github.com/jacaudi/ytdl-nfo/commit/144f5e10e1a47772c54b91cc1fb25a7afd750439) Changed from .yml to .yaml
- [`066425d`](https://github.com/jacaudi/ytdl-nfo/commit/066425d339f509155f61d1e6adebb0299af6baae) Added --config flag to get config folder location
- [`d348b8f`](https://github.com/jacaudi/ytdl-nfo/commit/d348b8fe4177b2f627754030426467a0a63b2046) Fixed config path in setuptools
- [`0972d0e`](https://github.com/jacaudi/ytdl-nfo/commit/0972d0e1b251550b933d7a0725a6cddb5596d636) Added pyyaml as a dependency
- [`eccc916`](https://github.com/jacaudi/ytdl-nfo/commit/eccc916077f5f058afa5739ff7494550c96a5d49) Package refactoring
- [`c7aeccd`](https://github.com/jacaudi/ytdl-nfo/commit/c7aeccdaf125e0ea03bf9cc98a2f3bf7e517c347) Added setuptools packaging and updated module help
- [`6f2e3b8`](https://github.com/jacaudi/ytdl-nfo/commit/6f2e3b8c5d4befef97fd5d1cdb72cf3b1b087e8d) Added Specific Extractor Option
- [`a685a75`](https://github.com/jacaudi/ytdl-nfo/commit/a685a7533c632de35d4ef0588ffd097ab3107f78) Changed to use _filename tag and remove .info
- [`69dc2b8`](https://github.com/jacaudi/ytdl-nfo/commit/69dc2b8ea23aff3c44f1ab164793bc21cc4b5273) Added directory parse support
- [`6934db4`](https://github.com/jacaudi/ytdl-nfo/commit/6934db4b7410012508138c7955393081c1354f75) Added repeat tags functionality and redid attributes
- [`8f1a4fa`](https://github.com/jacaudi/ytdl-nfo/commit/8f1a4fac0a095e7968e01f4c8bc5a7e76d479edf) Added NFO writing
- [`f0ef9b7`](https://github.com/jacaudi/ytdl-nfo/commit/f0ef9b7c8db796534623ca24336779d742a12f67) Create LICENSE.md
- [`d1475d3`](https://github.com/jacaudi/ytdl-nfo/commit/d1475d31fa1101a25a78266d7502ff30a443c311) Preliminary Youtube Extractor and NFO generation
- [`f2c9512`](https://github.com/jacaudi/ytdl-nfo/commit/f2c95126ec03500c74078c8043494bf1cb27f074) Initial Project Setup
