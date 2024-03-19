# CHANGELOG



## v1.0.1 (2024-03-19)

### Fix

* fix: bug with ref not in correct place (#102)

* fix: bug with ref not in correct place

* fix: update black

---------

Co-authored-by: Mark Harvey &lt;i31889@verisk.com&gt; ([`a93ad61`](https://github.com/harvey251/pydantic-lambda-handler/commit/a93ad61e3a7a817323239a076b023865cba74c31))


## v1.0.0 (2024-01-11)

### Breaking

* perf: bump to major version (#101)

BREAKING CHANGE: pydanticV2 ([`addf80e`](https://github.com/harvey251/pydantic-lambda-handler/commit/addf80eb7bdf8494c7132d305ffc5461a8914f35))


## v0.13.2 (2023-03-07)

### Fix

* fix: handle jsondecode error (#100) ([`00044de`](https://github.com/harvey251/pydantic-lambda-handler/commit/00044de03f88b4087816ce65cf55b3da561314fa))

### Unknown

* Return 400 on json decode error (#99) ([`866a328`](https://github.com/harvey251/pydantic-lambda-handler/commit/866a328bb9b262c3a2e0f4335e387730304b386b))


## v0.13.1 (2023-03-07)

### Fix

* fix: avoid json decode error if no body, (#98)

* fix: avoid json decode error if no body,

* fix: add is_base_64_encoded=False to response ([`99cf781`](https://github.com/harvey251/pydantic-lambda-handler/commit/99cf7812d6ded98fb41472e8b397b8f5e0c8f9eb))


## v0.13.0 (2023-02-15)

### Feature

* feat: add the base url (#96)

* feat: add the base url ([`ee7fc60`](https://github.com/harvey251/pydantic-lambda-handler/commit/ee7fc6081016a86419ec54ea4f72353aee011c2d))


## v0.12.8 (2023-01-31)

### Fix

* fix: add strings for ordering the hooks (#95) ([`e5f5c12`](https://github.com/harvey251/pydantic-lambda-handler/commit/e5f5c12a26454e1779c5ba1ee03bc9f042d40eff))


## v0.12.7 (2023-01-31)

### Fix

* fix: add pre return hook (#94) ([`19f889c`](https://github.com/harvey251/pydantic-lambda-handler/commit/19f889cd5a1623ab6a103a43e36c857eeac46194))


## v0.12.6 (2022-12-06)

### Fix

* fix: add info about openapi-spec-validator to docs (#93) ([`bbbbe11`](https://github.com/harvey251/pydantic-lambda-handler/commit/bbbbe11047a8c98a280633d785754f9be53c74a6))


## v0.12.5 (2022-12-06)

### Fix

* fix: add open api spec validation (#92)

* fix: add openapi-spec-validator to tests ([`0f1dc70`](https://github.com/harvey251/pydantic-lambda-handler/commit/0f1dc704f2bd031f19000a46fb4aed54a693786d))


## v0.12.4 (2022-11-09)

### Fix

* fix: add unions (#91)

* fix: add unions

* fix: linting errors

* fix: implicit None ([`5e0fd90`](https://github.com/harvey251/pydantic-lambda-handler/commit/5e0fd90d51a5fd24bae0342bb1d3374057141200))

### Unknown

* Fix description (#88)

* fix: add description when there are multiple errors

* fix: build docs ([`c72789b`](https://github.com/harvey251/pydantic-lambda-handler/commit/c72789b87a6d008927051f7a21d90bd561fd3847))


## v0.12.3 (2022-11-02)

### Fix

* fix: add docs for path parameters (#86) ([`90c053e`](https://github.com/harvey251/pydantic-lambda-handler/commit/90c053ee6175299f798deece40767faff5501dc4))


## v0.12.2 (2022-11-02)

### Fix

* fix: allow parsing of standard default types (#85)

* fix: allow parsing of standard default types

* fix: amend open api spec ([`90d12ff`](https://github.com/harvey251/pydantic-lambda-handler/commit/90d12fff7380097c7e0f4ebcc91887f98d294f74))


## v0.12.1 (2022-11-02)

### Fix

* fix: add error handling docs (#84) ([`123c543`](https://github.com/harvey251/pydantic-lambda-handler/commit/123c54325a73f3153973a1ae3d39b871d9ffdbcd))


## v0.12.0 (2022-11-02)

### Feature

* feat: add error handling (#83)

* feat: add error handling ([`2aaa550`](https://github.com/harvey251/pydantic-lambda-handler/commit/2aaa55078e78accf9ce27cc6b491bd940013103e))


## v0.11.1 (2022-10-25)

### Fix

* fix: add docs for query headers ([`5d6d741`](https://github.com/harvey251/pydantic-lambda-handler/commit/5d6d7418488d9d576c3c338aedb7c1496b8063df))


## v0.11.0 (2022-10-25)

### Feature

* feat: Multi Value Query model (#79)

* feat: add multivalue headers

* feat: add pydantic-core to requirements ([`44c4920`](https://github.com/harvey251/pydantic-lambda-handler/commit/44c4920c64c5f6dcc5364eeb11bb08f32fcfb5db))


## v0.10.2 (2022-10-11)

### Fix

* fix: add docs for headers and context (#77) ([`53da543`](https://github.com/harvey251/pydantic-lambda-handler/commit/53da543b59508a3e369d12af08265cda50d61802))


## v0.10.1 (2022-10-11)

### Fix

* fix: bug with cdk conf (#76) ([`1c5657b`](https://github.com/harvey251/pydantic-lambda-handler/commit/1c5657baa59ae31a7149bf76d504b11ab0d77e10))


## v0.10.0 (2022-10-03)

### Feature

* feat: add headers (#75) ([`979d7ff`](https://github.com/harvey251/pydantic-lambda-handler/commit/979d7ffa27c485577dad2c107409d620750fa0a6))

### Unknown

* Feat: Add Headers (#74) ([`d394de2`](https://github.com/harvey251/pydantic-lambda-handler/commit/d394de259e0a63864ab9898cc6b246327795570a))


## v0.9.0 (2022-09-27)

### Feature

* feat: add handlers folder (#73)

* feat: add handlers folder

* feat: add handlers folder ([`e41a6b9`](https://github.com/harvey251/pydantic-lambda-handler/commit/e41a6b9b36c99c147faa1636ef0e9396408b69cf))


## v0.8.11 (2022-09-24)

### Fix

* fix: capture error for mock requests (#72)

* fix: capture error for mock requests ([`ca961da`](https://github.com/harvey251/pydantic-lambda-handler/commit/ca961da9f618b537950edab9ec58b3949ce50f3f))


## v0.8.10 (2022-09-21)

### Fix

* fix: set event body as optional (#70)

* fix: set event body as optional

* test: set event body as optional ([`7d7ee58`](https://github.com/harvey251/pydantic-lambda-handler/commit/7d7ee58cae07fee08cc2a696a07570f389e649bb))


## v0.8.9 (2022-09-21)

### Fix

* fix: allow &#34;name&#34; not to be set in conf (#69)

* fix: allow &#34;name&#34; not to be set in conf

* fix: add mock ([`67bb4e4`](https://github.com/harvey251/pydantic-lambda-handler/commit/67bb4e4a514b0d1ca69bd7b31f978e691ce6f971))


## v0.8.8 (2022-09-07)

### Fix

* fix: run checks in ci (#66)

* fix: run checks in ci

* fix: run gen open api spec ([`17f78c6`](https://github.com/harvey251/pydantic-lambda-handler/commit/17f78c6a986446114ecd44779f0c6c6461273d53))


## v0.8.7 (2022-09-07)

### Fix

* fix: add index location and remove prints (#65) ([`00abacc`](https://github.com/harvey251/pydantic-lambda-handler/commit/00abacc35ccbfbcd12d00dbec8c2d38c89d9abd5))


## v0.8.6 (2022-09-05)

### Fix

* fix: add generate_event (#64) ([`26e026f`](https://github.com/harvey251/pydantic-lambda-handler/commit/26e026f9440e07b5d4d34c240dafc9abf9f4c144))


## v0.8.5 (2022-09-05)

### Fix

* fix: use response model (#63)

* fix: use response model

* fix: refactor to be simpler ([`ad3b17c`](https://github.com/harvey251/pydantic-lambda-handler/commit/ad3b17c1f326dd7e9bf8153d3dc19a65d07bdd61))


## v0.8.4 (2022-09-01)

### Fix

* fix: Add debug logs (#62)

* fix: add tests

* fix: add debug logs ([`e8ddaaf`](https://github.com/harvey251/pydantic-lambda-handler/commit/e8ddaaf8a12fc2577784dfa4b4f970abdc2fbce3))


## v0.8.3 (2022-08-31)

### Ci

* ci: add pypi badge (#60) ([`0e0884f`](https://github.com/harvey251/pydantic-lambda-handler/commit/0e0884f0104ad909a8f31d8321bdd8ff7dc62c52))

* ci: add code cov (#59)

* ci: add code cov

* ci: add code cov to readme ([`10dd547`](https://github.com/harvey251/pydantic-lambda-handler/commit/10dd54715bf9d87f4cb0cd0e26fa08a0634a17bf))

### Fix

* fix: add logging on error (#61)

* fix: add logging on error ([`4e65733`](https://github.com/harvey251/pydantic-lambda-handler/commit/4e65733bb0d54111127c7bde23d4abf102ec6aa8))

### Unknown

* Update README.md ([`2c89b7a`](https://github.com/harvey251/pydantic-lambda-handler/commit/2c89b7a8e1bbcdd88f9178799d169c19df9c9a8a))


## v0.8.2 (2022-08-30)

### Fix

* fix: add pypi repo details (#58) ([`4af957f`](https://github.com/harvey251/pydantic-lambda-handler/commit/4af957fac980ec1b9dc063ef5933582e609001d2))


## v0.8.1 (2022-08-30)

### Feature

* feat: remove docstring ([`8bde2c4`](https://github.com/harvey251/pydantic-lambda-handler/commit/8bde2c46c0c845c316c868874ad65d2377bdf954))

* feat: amend version ([`043310a`](https://github.com/harvey251/pydantic-lambda-handler/commit/043310a7234744fcb8638ce94a2b0c4ac4c3c671))

### Fix

* fix: allow list response (#57)

* fix: allow list response

* test: list response schema ([`8045667`](https://github.com/harvey251/pydantic-lambda-handler/commit/80456671d322374c6aeb45121afa8372ed184e22))

* fix: ignore ([`1cc2470`](https://github.com/harvey251/pydantic-lambda-handler/commit/1cc2470507ccc18b2035fca4492ed5923dac24a0))

### Unknown

* Merge remote-tracking branch &#39;origin/main&#39; ([`191c86b`](https://github.com/harvey251/pydantic-lambda-handler/commit/191c86b1c80200f26c63239223add87950364cb4))

* Fix: release (#56)

* fix: ignore

* fix: ignore

* 0.7.0

Automatically generated by python-semantic-release

* fix: add doc string

* 0.7.1

Automatically generated by python-semantic-release

* fix: remove doc string

* 0.7.2

Automatically generated by python-semantic-release

* fix: only publish on main

Co-authored-by: semantic-release &lt;semantic-release&gt; ([`912fe91`](https://github.com/harvey251/pydantic-lambda-handler/commit/912fe9199f4e8cc9dced479588670e99885d987c))


## v0.7.1 (2022-08-30)

### Feature

* feat: refactor cdk conf command (#50)

* fix: refactored cdk conf output

* fix: refactored cdk conf output

* feat: refactor cdk conf command

* fix: amend path ([`473671f`](https://github.com/harvey251/pydantic-lambda-handler/commit/473671fcfe76f3c1d632bc3b9f758aaf98508c2e))

* feat: add cdk conf command (#48)

* feat: add semantic release

* feat: add cdk conf command ([`913ab28`](https://github.com/harvey251/pydantic-lambda-handler/commit/913ab280bd691e9e38f6e643d41833c37f401389))

### Fix

* fix: seperate out dev requirements (#53) ([`98f6a87`](https://github.com/harvey251/pydantic-lambda-handler/commit/98f6a87bc7e5325cea8ed6b1deed19a9ec97cc1b))

* fix: add docs (#52) ([`ca204d8`](https://github.com/harvey251/pydantic-lambda-handler/commit/ca204d86a8ee8be37180957642f3fb617e375cea))

* fix: add docs (#51) ([`aef6813`](https://github.com/harvey251/pydantic-lambda-handler/commit/aef68135f574c8f47ef48e027e69c1a73ee375fd))


## v0.6.3 (2022-08-23)

### Ci

* ci: add badge to readme (#37) ([`77967c2`](https://github.com/harvey251/pydantic-lambda-handler/commit/77967c2a4b4338e54c5ab1b43a8a50d92f23b335))

### Feature

* feat: add response body (#45)

* feat: add response body

* fix: remove import ([`4510db7`](https://github.com/harvey251/pydantic-lambda-handler/commit/4510db71090dc48654e3ba9899ed2d91290cb4dc))

### Fix

* fix: add semantic release (#47) ([`5999b65`](https://github.com/harvey251/pydantic-lambda-handler/commit/5999b65cc3437294271cb94cb4e80b78a303214c))

* fix: Cli gen open api spec (#46)

* fix: remove import

* fix:add args ([`34ab7fc`](https://github.com/harvey251/pydantic-lambda-handler/commit/34ab7fc8e1ba8f5b4f53643b7fea2acd4c9d93d2))

* fix: contxt to func (#42) ([`619ea12`](https://github.com/harvey251/pydantic-lambda-handler/commit/619ea123c4a5c27e6f57e3625d231cf8d5bfd907))

* fix: add open api spec (#41) ([`a576cd5`](https://github.com/harvey251/pydantic-lambda-handler/commit/a576cd5855630d65f0022b21d83ab9412e9d3cbc))

* fix: separate out mock requests (#40) ([`8238aa5`](https://github.com/harvey251/pydantic-lambda-handler/commit/8238aa556c19789f381f42a831fc2132aefce519))

* fix: separate out cdk_conf (#39) ([`5bfed51`](https://github.com/harvey251/pydantic-lambda-handler/commit/5bfed51debc7dc990a389fe26ff3ddc25dd6b633))

* fix: Add lambda context (#38)

* add badge to readme

* fix: allow gen open api spec to accept locations

* fix: add lambda context

* fix: flake8 ([`01fed1a`](https://github.com/harvey251/pydantic-lambda-handler/commit/01fed1addf5c770ec9c4a7a58be3c8d5f4fda747))


## v0.6.2 (2022-08-15)

### Fix

* fix: add a space ([`fd182ac`](https://github.com/harvey251/pydantic-lambda-handler/commit/fd182acd14017b320d480a5cb8b7a6218501ac42))

* fix: add a space ([`1cb8651`](https://github.com/harvey251/pydantic-lambda-handler/commit/1cb8651e67a116ff4e164bda94168dbd64ac620e))

* fix: add a space ([`8e4a006`](https://github.com/harvey251/pydantic-lambda-handler/commit/8e4a0066e649aa7ea126e9ce9ba53cee3709b46f))

### Unknown

* fix:update gitignore ([`938ecdc`](https://github.com/harvey251/pydantic-lambda-handler/commit/938ecdc69e640adecbb693ab3c72992eecc9b54b))


## v0.6.0 (2022-08-15)

### Feature

* feat: add request body to open api spec (#35) ([`47891da`](https://github.com/harvey251/pydantic-lambda-handler/commit/47891da9ec80bfe312dc8489b2565333f9e9ba3b))


## v0.5.1 (2022-08-14)

### Fix

* fix: merge post and get (#33) ([`f4cff6f`](https://github.com/harvey251/pydantic-lambda-handler/commit/f4cff6f68ad1185f120cbd542aa946cf128a6a75))


## v0.5.0 (2022-08-14)

### Feature

* feat: add post data (#32)

* feat: add post data

* fix: import error ([`544b1e1`](https://github.com/harvey251/pydantic-lambda-handler/commit/544b1e16882de23c6ddd9d791dc7255ac9d46650))


## v0.4.1 (2022-08-12)

### Fix

* fix: add pydantic core test (#31) ([`368deae`](https://github.com/harvey251/pydantic-lambda-handler/commit/368deae1976862a975bafaf23b18333e1ac3b68a))


## v0.4.0 (2022-08-12)

### Feature

* feat: add query (#30)

* fix: add check

* fix: remove import

* feat: add querys

* fix: refactor ([`fcfa161`](https://github.com/harvey251/pydantic-lambda-handler/commit/fcfa161d73cf78de5716a3449ac3ac33a84908c2))


## v0.3.1 (2022-08-11)

### Fix

* fix: add check for redeclaration of path (#29)

* fix: add check

* fix: remove import ([`a9671c6`](https://github.com/harvey251/pydantic-lambda-handler/commit/a9671c6f4c5ca6d61032e6ebbed986df3dae536b))


## v0.3.0 (2022-08-11)

### Feature

* feat: move gen open api spec into a hook (#28)

* feat: move gen open api spec into a hook

* ci: amend mypy location

* ci: amend class name

* ci: try this

* ci: try ignoreing ([`a2e34b8`](https://github.com/harvey251/pydantic-lambda-handler/commit/a2e34b8736a6303009a7d8ea64cefa2afd3a915a))

### Unknown

* 19 create a test to be run against aws locally (#26)

* feat: add task to deploy

* fix: correct linting errors

* feat: add resources dynamically

* feat: update tests

* feat: add task to deploy (#23)

* feat: add task to deploy

* fix: remove url

* fix: amend flake8 issues

* fix: refactor out some complexity

* ci: amend github nox ([`21d1d4a`](https://github.com/harvey251/pydantic-lambda-handler/commit/21d1d4aca358b0f288893a9d75469a43aa7b6b25))


## v0.2.0 (2022-07-31)

### Documentation

* docs: improve Vision statement (#22) ([`af7c95f`](https://github.com/harvey251/pydantic-lambda-handler/commit/af7c95f73b3d71b56948b50ddacf5aaa52e7ebd7))

### Feature

* feat: add task to deploy (#23)

* feat: add task to deploy ([`ea67f71`](https://github.com/harvey251/pydantic-lambda-handler/commit/ea67f71001552b4eeff8d08a9379c7e271be7921))

### Unknown

* Preflint (#18)

fix: preflint improvements ([`3fce545`](https://github.com/harvey251/pydantic-lambda-handler/commit/3fce54571e89794ed00844da89dfdc55809e2fc6))


## v0.1.0 (2022-07-13)

### Ci

* ci: add runs on (#5)

* ci: run nox ([`c7a4f7b`](https://github.com/harvey251/pydantic-lambda-handler/commit/c7a4f7b2120d81bbef3410a324eb2eaedcded475))

* ci: turn on ci

* Add get request

* ci: update to use main ([`da077fb`](https://github.com/harvey251/pydantic-lambda-handler/commit/da077fbb79e20a7a7652bea98aa142a186214fac))

### Feature

* feat: add open api spec

feat: add path parameters ([`a6b5ff9`](https://github.com/harvey251/pydantic-lambda-handler/commit/a6b5ff96bf4695c6dd9ee2e73492a97134323361))

* feat: add error message with invalid params (#8) ([`0ad9ff1`](https://github.com/harvey251/pydantic-lambda-handler/commit/0ad9ff13e512a0904624a8f806cb787393040650))

* feat: add open api spec (#7) ([`82db24b`](https://github.com/harvey251/pydantic-lambda-handler/commit/82db24b23025939188ee6ed728bbc31d28552124))

### Fix

* fix: release on main (#12) ([`c142360`](https://github.com/harvey251/pydantic-lambda-handler/commit/c142360be3c88a568969625ae5c08d7daf83b8ba))

* fix: add default required values for open api spec (#11)

* fix: add default required values for open api spec ([`e380eb9`](https://github.com/harvey251/pydantic-lambda-handler/commit/e380eb90ce5c3a21b9790742497ec88a8805ad40))

* fix: add init (#10) ([`c20f3bb`](https://github.com/harvey251/pydantic-lambda-handler/commit/c20f3bb437e9ac38e4e50c89981c32afbd44aedb))

### Unknown

* Release package (#14)

fix: release on main ([`6bbff45`](https://github.com/harvey251/pydantic-lambda-handler/commit/6bbff45641cb0107f06202f620f52ef69d9a2700))

* Release package (#13)

* ci: release on main ([`b4df791`](https://github.com/harvey251/pydantic-lambda-handler/commit/b4df7919e8b60f744871114a1e9687de5713c66f))

* First steps (#6) ([`6bb81a3`](https://github.com/harvey251/pydantic-lambda-handler/commit/6bb81a3c558d39563e9faa2cb9428af2cd90ddf2))

* Update main.yml (#4) ([`fb0ad8c`](https://github.com/harvey251/pydantic-lambda-handler/commit/fb0ad8cf5a119b403b6ecd7cb160308262e2dd75))

* Add decorator for get request ([`8c3bee5`](https://github.com/harvey251/pydantic-lambda-handler/commit/8c3bee5681f788905e6ec602b7e73a9f27ec49e8))

* Setup ci (#1)

ci: initial setup ([`e54d805`](https://github.com/harvey251/pydantic-lambda-handler/commit/e54d805d3119fdcee46fb2c414297b68fc5161ca))

* Initial commit ([`801fb3f`](https://github.com/harvey251/pydantic-lambda-handler/commit/801fb3f8aff3798906cace7e4b10f9cc1e637718))
