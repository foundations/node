{
  # 'force_load' means to include the static libs into the shared lib or
  # executable. Therefore, it is enabled when building:
  # 1. The executable and it uses static lib (cctest and node)
  # 2. The shared lib
  # Linker optimizes out functions that are not used. When force_load=true,
  # --whole-archive,force_load and /WHOLEARCHIVE are used to include
  # all obj files in static libs into the executable or shared lib.
  'variables': {
    'variables': {
      'variables': {
        'force_load%': 'true',
        'current_type%': '<(_type)',
      },
      'force_load%': '<(force_load)',
      'conditions': [
        ['current_type=="static_library"', {
          'force_load': 'false',
        }],
        [ 'current_type=="executable" and node_target_type=="shared_library"', {
          'force_load': 'false',
        }]
      ],
    },
    'force_load%': '<(force_load)',
  },
  # Putting these explicitly here so not to be dependant on common.gypi.
  'cflags': [ '-Wall', '-Wextra', '-Wno-unused-parameter', ],
  'xcode_settings': {
    'WARNING_CFLAGS': [
      '-Wall',
      '-Wendif-labels',
      '-W',
      '-Wno-unused-parameter',
    ],
  },
  'conditions': [
    [ 'node_shared=="false"', {
      'msvs_settings': {
        'VCManifestTool': {
          'EmbedManifest': 'true',
          'AdditionalManifestFiles': 'src/res/node.exe.extra.manifest'
        }
      },
    }, {
      'defines': [
        'NODE_SHARED_MODE',
      ],
    }],
    [ 'OS=="win"', {
      'defines!': [
        'NODE_PLATFORM="win"',
      ],
      'defines': [
        'FD_SETSIZE=1024',
        # we need to use node's preferred "win32" rather than gyp's preferred "win"
        'NODE_PLATFORM="win32"',
        # Stop <windows.h> from defining macros that conflict with
        # std::min() and std::max().  We don't use <windows.h> (much)
        # but we still inherit it from uv.h.
        'NOMINMAX',
        '_UNICODE=1',
      ],
    }, { # POSIX
      'defines': [ '__POSIX__' ],
    }],

    [ 'node_enable_d8=="true"', {
      'dependencies': [ 'deps/v8/gypfiles/d8.gyp:d8' ],
    }],
    [ 'node_use_bundled_v8=="true"', {
      'conditions': [
        [ 'build_v8_with_gn=="true"', {
          #'dependencies': ['deps/v8/gypfiles/v8-monolithic.gyp:v8_monolith'],
        }, {
          'dependencies': [
            #'deps/v8/gypfiles/v8.gyp:v8',
            #'deps/v8/gypfiles/v8.gyp:v8_libplatform',
          ],
        }],
      ],
    }],
    [ 'node_use_v8_platform=="true"', {
      'defines': [
        'NODE_USE_V8_PLATFORM=1',
      ],
    }, {
      'defines': [
        'NODE_USE_V8_PLATFORM=0',
      ],
    }],
    [ 'node_tag!=""', {
      'defines': [ 'NODE_TAG="<(node_tag)"' ],
    }],
    [ 'node_v8_options!=""', {
      'defines': [ 'NODE_V8_OPTIONS="<(node_v8_options)"'],
    }],
    [ 'node_release_urlbase!=""', {
      'defines': [
        'NODE_RELEASE_URLBASE="<(node_release_urlbase)"',
      ]
    }],
    ['node_target_type=="shared_library"', {
      'direct_dependent_settings': {
        'defines': [
          'USING_UV_SHARED=1',
          'BUILDING_NODE_EXTENSION=1',
        ],
      },
    }],
    ['clang==1', {
      'cflags': ['-Wno-error=missing-declarations', '-Wno-error=array-bounds'],
    }],
    [ 'v8_enable_i18n_support==1', {
      'defines': [ 'NODE_HAVE_I18N_SUPPORT=1' ],
      'dependencies': [
        '../icu/icu.gyp:icui18n',
        '../icu/icu.gyp:icuuc',
      ],
      'conditions': [
        [ 'icu_small=="true"', {
          'defines': [ 'NODE_HAVE_SMALL_ICU=1' ],
      }]],
    }],
    [ 'node_use_bundled_v8=="true" and \
       node_enable_v8_vtunejit=="true" and (target_arch=="x64" or \
       target_arch=="ia32" or target_arch=="x32")', {
      'defines': [ 'NODE_ENABLE_VTUNE_PROFILING' ],
      'dependencies': [
        'deps/v8/gypfiles/v8vtune.gyp:v8_vtune'
      ],
    }],
    [ 'node_no_browser_globals=="true"', {
      'defines': [ 'NODE_NO_BROWSER_GLOBALS' ],
    } ],
    [ 'node_use_bundled_v8=="true" and v8_postmortem_support=="true" and force_load=="true"', {
      'xcode_settings': {
        'OTHER_LDFLAGS': [
          '-Wl,-force_load,<(v8_base)',
        ],
      },
    }],
    [ 'node_shared_zlib=="false"', {
      'dependencies': [ 'deps/zlib/zlib.gyp:zlib' ],
      'conditions': [
        [ 'force_load=="true"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-force_load,<(PRODUCT_DIR)/<(STATIC_LIB_PREFIX)'
                  'zlib<(STATIC_LIB_SUFFIX)',
            ],
          },
          'msvs_settings': {
            'VCLinkerTool': {
              'AdditionalOptions': [
                '/WHOLEARCHIVE:obj\\third_party\\node-nw\\deps\\zlib\\zlib<(STATIC_LIB_SUFFIX)',
              ],
            },
          },
          'conditions': [
            ['OS!="aix" and node_shared=="false"', {
              'ldflags': [
                '-Wl,--whole-archive,<(obj_dir)/deps/zlib/<(STATIC_LIB_PREFIX)'
                    'zlib<(STATIC_LIB_SUFFIX)',
                '-Wl,--no-whole-archive',
              ],
            }],
          ],
        }],
      ],
    }],

    [ 'node_shared_http_parser=="false"', {
      'dependencies': [ 'deps/http_parser/http_parser.gyp:http_parser' ],
    }],

    [ 'node_shared_cares=="false"', {
      'dependencies': [ 'deps/cares/cares.gyp:cares' ],
    }],

    [ 'node_shared_libuv=="false"', {
      'dependencies': [ 'deps/uv/uv.gyp:libuv' ],
      'conditions': [
        [ 'force_load=="true"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-force_load,<(PRODUCT_DIR)/<(STATIC_LIB_PREFIX)'
                  'uv<(STATIC_LIB_SUFFIX)',
            ],
          },
          'msvs_settings': {
            'VCLinkerTool': {
              'AdditionalOptions': [
                '/WHOLEARCHIVE:obj\\third_party\\node-nw\\deps\\uv\\libuv<(STATIC_LIB_SUFFIX)',
              ],
            },
          },
          'conditions': [
            ['OS!="aix" and node_shared=="false"', {
              'ldflags': [
                '-Wl,--whole-archive,<(obj_dir)/deps/uv/<(STATIC_LIB_PREFIX)'
                    'uv<(STATIC_LIB_SUFFIX)',
                '-Wl,--no-whole-archive',
              ],
            }],
          ],
        }],
      ],
    }],

    [ 'node_shared_nghttp2=="false"', {
      'dependencies': [ 'deps/nghttp2/nghttp2.gyp:nghttp2' ],
    }],
    [ 'OS=="win" and component=="shared_library"', {
      'libraries': [ '<(PRODUCT_DIR)/../nw/v8.dll.lib' ]
    }],

    [ 'OS=="mac"', {
      # linking Corefoundation is needed since certain OSX debugging tools
      # like Instruments require it for some features
      'libraries': [ '-framework CoreFoundation' ],
      'defines!': [
        'NODE_PLATFORM="mac"',
      ],
      'defines': [
        # we need to use node's preferred "darwin" rather than gyp's preferred "mac"
        'NODE_PLATFORM="darwin"',
      ],
     'postbuilds': [
       {
         'postbuild_name': 'Fix Framework Link',
         'action': [
           'install_name_tool',
           '-change',
           '@executable_path/../Versions/<(version_full)/<(mac_product_name) Framework.framework/<(mac_product_name) Framework',
           '@loader_path/<(mac_product_name) Framework',
           '${BUILT_PRODUCTS_DIR}/${EXECUTABLE_PATH}'
         ],
       },
     ],
    }],
    [ 'OS=="freebsd"', {
      'libraries': [
        '-lutil',
        '-lkvm',
      ],
    }],
    [ 'OS=="aix"', {
      'defines': [
        '_LINUX_SOURCE_COMPAT',
      ],
      'conditions': [
        [ 'force_load=="true"', {

          'actions': [
            {
              'action_name': 'expfile',
              'inputs': [
                '<(obj_dir)'
              ],
              'outputs': [
                '<(PRODUCT_DIR)/node.exp'
              ],
              'action': [
                'sh', 'tools/create_expfile.sh',
                      '<@(_inputs)', '<@(_outputs)'
              ],
            }
          ],
          'ldflags': ['-Wl,-bE:<(PRODUCT_DIR)/node.exp', '-Wl,-brtl'],
        }],
      ],
    }],
    [ 'OS=="solaris"', {
      'libraries': [
        '-lkstat',
        '-lumem',
      ],
      'defines!': [
        'NODE_PLATFORM="solaris"',
      ],
      'defines': [
        # we need to use node's preferred "sunos"
        # rather than gyp's preferred "solaris"
        'NODE_PLATFORM="sunos"',
      ],
    }],
    [ 'OS=="linux"', {
      'cflags': [ "-Wno-unused-result" ],
    }],
    [ 'OS=="linux" and component == "shared_library"', {
          'ldflags': [ '-L<(PRODUCT_DIR)/../nw/lib/', '-lv8',
                      '-Wl,--whole-archive <(V8_LIBBASE)',
                      '<(V8_PLTFRM)',
                      '-Wl,--no-whole-archive' ]
    }],
    [ 'OS=="linux" and component != "shared_library"', {
          'ldflags': [ '-L<(PRODUCT_DIR)/../nw/lib/', '-lnw',
                      '-Wl,--whole-archive',
                      '<(LIBCXXABI)', '<(LIBCXX)',
                      '-Wl,--no-whole-archive'
                     ]
    }],
    [ 'OS=="mac" and component == "shared_library"', {
      'xcode_settings': {
        'OTHER_LDFLAGS': [
          '-L<(PRODUCT_DIR)/../nw/', '-lv8',
          '<(PRODUCT_DIR)/../nw/nwjs\ Framework.framework/nwjs\ Framework',
                  '-Wl,-force_load <(V8_LIBBASE)',
                  '-Wl,-force_load <(V8_PLTFRM)',
        ],
      },
      'postbuilds': [
        {
          'postbuild_name': 'Fix iculib Link',
          'action': [
            'install_name_tool',
            '-change',
            '/usr/local/lib/libicuuc.dylib',
            '@rpath/libicuuc.dylib',
            '${BUILT_PRODUCTS_DIR}/${EXECUTABLE_PATH}'
          ],
        },
        {
          'postbuild_name': 'Fix iculib Link2',
          'action': [
            'install_name_tool',
            '-change',
            '/usr/local/lib/libicui18n.dylib',
            '@rpath/libicui18n.dylib',
            '${BUILT_PRODUCTS_DIR}/${EXECUTABLE_PATH}'
          ],
        },
      ],
    }],
    [ 'OS=="mac" and component != "shared_library"', {
     'xcode_settings': {
       'OTHER_LDFLAGS': [
         '<(PRODUCT_DIR)/../nw/nwjs\ Framework.framework/nwjs\ Framework',
                 '-Wl,-force_load <(V8_LIBBASE)',
                 '-Wl,-force_load <(V8_PLTFRM)',
       ],
     },
    }],
    [ 'OS in "mac freebsd linux" and node_shared=="false"'
        ' and coverage=="true"', {
      'ldflags': [ '--coverage',
                   '-g',
                   '-O0' ],
      'cflags': [ '--coverage',
                   '-g',
                   '-O0' ],
      'cflags!': [ '-O3' ],
      'xcode_settings': {
        'OTHER_LDFLAGS': [
          '--coverage',
        ],
        'OTHER_CFLAGS+': [
          '--coverage',
          '-g',
          '-O0'
        ],
      }
    }],
    [ 'OS=="sunos"', {
      'ldflags': [ '-Wl,-M,/usr/lib/ld/map.noexstk' ],
    }],
    [ 'OS in "freebsd linux"', {
      'ldflags': [ '-Wl,-z,relro',
                   '-Wl,-z,now' ]
    }],
    [ 'node_use_openssl=="true"', {
      'defines': [ 'HAVE_OPENSSL=1' ],
      'conditions': [
        ['openssl_fips != ""', {
          'defines': [ 'NODE_FIPS_MODE' ],
        }],
        [ 'node_shared_openssl=="false"', {
          'dependencies': [
            './deps/openssl/openssl.gyp:openssl',

            # For tests
            #'./deps/openssl/openssl.gyp:openssl-cli',
          ],
          'conditions': [
            # -force_load or --whole-archive are not applicable for
            # the static library
            [ 'force_load=="true"', {
              'xcode_settings': {
                'OTHER_LDFLAGS': [
                  #'-Wl,-force_load,<(PRODUCT_DIR)/<(openssl_product)',
                ],
              },
              'msvs_settings': {
                'VCLinkerTool': {
                  'AdditionalOptions': [
                    '/WHOLEARCHIVE:obj\\third_party\\node-nw\\deps\\openssl\\openssl<(STATIC_LIB_SUFFIX)',
                  ],
                },
              },
              'conditions': [
                ['OS in "linux freebsd" and node_shared=="false"', {
                  'ldflags': [
                    #'-Wl,--whole-archive,'
                    #  '<(obj_dir)/deps/openssl/<(openssl_product)',
                    #'-Wl,--no-whole-archive',
                  ],
                }],
                # openssl.def is based on zlib.def, zlib symbols
                # are always exported.
                ['use_openssl_def==1', {
                  'sources': ['<(SHARED_INTERMEDIATE_DIR)/openssl.def'],
                }],
                ['OS=="win" and use_openssl_def==0', {
                  'sources': ['deps/zlib/win32/zlib.def'],
                }],
              ],
            }],
          ],
        }]]

    }, {
      'defines': [ 'HAVE_OPENSSL=0' ]
    }],

  ],
}
