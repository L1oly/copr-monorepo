%global luato_commit        df0c6f2d1cce2051b4711d36067619eda7933683
%global ncrequest_commit    40d40224842a080039d2a76710fbedb20ee002ac
%global wavsen_commit       bd8a72e0f68fabc42f3d123623787398ed28dbe4
%global qextra_commit       650cb670c15c2f34a9cf0dedd52447df7b56e761
# Leave empty (%%global qml_material_commit %%{nil}) to use the installed qmlmaterial package
%global qml_material_commit 98b8acd3e0bd57ca0710f2712e4dfa3fcef13113

%global toolchain clang
%global _lto_cflags %{nil}

Name:           waywallen
Version:        0.4.4
Release:        1%{?dist}
Summary:        Wallpaper manager for Linux
License:        MIT
URL:            https://github.com/waywallen/waywallen
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/litocpp/luato/archive/%{luato_commit}/luato-%{luato_commit}.tar.gz
Source2:        https://github.com/hypengw/ncrequest/archive/%{ncrequest_commit}/ncrequest-%{ncrequest_commit}.tar.gz
Source3:        https://github.com/hypengw/wavsen/archive/%{wavsen_commit}/wavsen-%{wavsen_commit}.tar.gz
Source4:        https://github.com/hypengw/QExtra/archive/%{qextra_commit}/QExtra-%{qextra_commit}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  cargo
BuildRequires:  lito >= 0.8.5
BuildRequires:  clang >= 22
BuildRequires:  lld
BuildRequires:  llvm
BuildRequires:  vulkan-headers
BuildRequires:  vulkan-loader-devel
BuildRequires:  sqlite-devel
BuildRequires:  libzstd-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtgrpc-devel
BuildRequires:  qt6-qtwebsockets-devel
BuildRequires:  qt6-qttools-devel
# ffmpeg / mesa: adjust to whatever the build actually links against
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libgbm-devel

Requires:       vulkan-loader
Requires:       qt6-qtdeclarative
Requires:       qt6-qtgrpc
Requires:       qt6-qtwebsockets
Requires:       hicolor-icon-theme

%if "%{?qml_material_commit}" != ""
BuildRequires:  git-lfs
BuildRequires:  qt6-qtshadertools-devel
%else
BuildRequires:  qmlmaterial-devel
Requires:       qmlmaterial
%endif

Suggests:       waywallen-display





%description
Waywallen is a wallpaper manager for Linux. Install waywallen-display for
layer-shell based compositors.

%prep
%setup -q -c -T
mkdir waywallen luato ncrequest wavsen QExtra
tar -xf %{SOURCE0} -C waywallen  --strip-components=1
tar -xf %{SOURCE1} -C luato      --strip-components=1
tar -xf %{SOURCE2} -C ncrequest  --strip-components=1
tar -xf %{SOURCE3} -C wavsen     --strip-components=1
tar -xf %{SOURCE4} -C QExtra     --strip-components=1

%if "%{?qml_material_commit}" != ""
git clone https://github.com/hypengw/QmlMaterial.git QmlMaterial
git -C QmlMaterial checkout %{qml_material_commit}
git -C QmlMaterial lfs install --local
git -C QmlMaterial lfs pull
%endif

cd waywallen
mkdir -p .lito
cat > .lito/config.toml << EOF
[patch."https://github.com/litocpp/luato.git"]
path = "../luato"

[patch."https://github.com/hypengw/wavsen.git"]
path = "../wavsen"

[patch."https://github.com/hypengw/ncrequest.git"]
path = "../ncrequest"

[patch."https://github.com/hypengw/QExtra.git"]
path = "../QExtra"

EOF

%if "%{?qml_material_commit}" != ""
cat >> .lito/config.toml << EOF
[patch."https://github.com/hypengw/QmlMaterial.git"]
path = "../QmlMaterial"
EOF
%else
cat >> .lito/config.toml << EOF
[tools.cmake.overrides.qml_material]
source = "installed"
EOF
%endif

cargo fetch --target host-tuple
lito fetch --all-features

%build
%set_build_flags
export LIBSQLITE3_SYS_USE_PKG_CONFIG=1
export ZSTD_SYS_USE_PKG_CONFIG=1

CXXFLAGS="${CXXFLAGS//-Wp,-D_FORTIFY_SOURCE=3/}"
export CXXFLAGS

RUSTFLAGS+=" -C link-arg=-fuse-ld=lld"
export RUSTFLAGS

lito -C %{name} build --profile plain --use-env-flags

%install
lito -C %{name} install --profile plain --prefix %{buildroot}%{_prefix} --no-build

%files
%license waywallen/LICENSE
%{_bindir}/waywallen*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Fri Oct 16 2026 Your Name <you@example.com> - 0.4.4-1
- Initial RPM package (converted from Arch PKGBUILD)
