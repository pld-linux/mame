# TODO: is qt optional? (either as bcond, or qt-less version)
#
# https://github.com/mamedev/mame/issues/7046
# Conditional build:
%bcond_with	system_lua		# build system lua (needs LUA build as C++)
#
%define		fver	%(echo %{version} | tr -d .)
Summary:	MAME - Multiple Arcade Machine Emulator
Summary(pl.UTF-8):	MAME (Multiple Arcade Machine Emulator) - emulator wielu automatów do gier
Name:		mame
Version:	0.283
Release:	0.1
License:	GPL v2+ (BSD for core part, LGPL v2.1+/GPL v2+ for some drivers)
Group:		X11/Applications/Games
#Source0Download: https://www.mamedev.org/release.html
Source0:	https://github.com/mamedev/mame/archive/mame%{fver}/%{name}-%{version}.tar.gz
# Source0-md5:	0ba4eb1221411078c94186619ab964d3
Patch0:		lua-cxx.patch
URL:		https://www.mamedev.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt6Core-devel >= 5
BuildRequires:	Qt6Gui-devel >= 5
BuildRequires:	Qt6Widgets-devel >= 5
BuildRequires:	SDL2-devel >= 2
BuildRequires:	SDL2_ttf-devel >= 2
BuildRequires:	alsa-lib-devel
BuildRequires:	asio-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flac-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	GLM-devel
BuildRequires:	libjpeg-devel
%{?with_system_lua:BuildRequires:	lua54-devel >= 5.4.7}
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	portmidi-devel
BuildRequires:	pugixml-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	rapidjson-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	unzip
BuildRequires:	utf8proc-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Requires:	%{name}-data = %{version}-%{release}
Suggests:	gmameui
Obsoletes:	sdlhazemd < 0.15
Obsoletes:	sdlmame < 0.137
Obsoletes:	xmame < 0.107
Obsoletes:	xmame-SDL < 0.107
Obsoletes:	xmame-common < 0.107
Obsoletes:	xmame-qtmame < 0.107
Obsoletes:	xmame-svgalib < 0.107
Obsoletes:	xmame-x11 < 0.107
Obsoletes:	xmame-xmess-SDL < 0.107
Obsoletes:	xmame-xmess-svgalib < 0.107
Obsoletes:	xmame-xmess-x11 < 0.107
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# linker memory exhausted on x86_64 after reaching 23GB of virt mem
%define		_enable_debug_packages	0

%description
MAME stands for Multiple Arcade Machine Emulator.

MAME's purpose is to preserve decades of video-game history. As gaming
technology continues to rush forward, MAME prevents these important
"vintage" games from being lost and forgotten. This is achieved by
documenting the hardware and how it functions. The source code to MAME
serves as this documentation. The fact that the games are playable
serves primarily to validate the accuracy of the documentation (how
else can you prove that you have recreated the hardware faithfully?).

%description -l pl.UTF-8
MAME to skrót od Multiple Arcade Machine Emulator - emulatora wielu
automatów do gier.

Celem MAME jest zachowanie dziesięcioleci historii gier wideo.
Jakkolwiek techonologia gier cały czas szybko się posuwa, MAME chroni
te ważne, "starodawne" gry od zapomnienia. Można to osiągnąć poprzez
dokumentowanie sprzętu i sposobu jego funkcjonowania. Kod źródłowy
MAME służy jako ta dokumentacja. Fakt, że w gry da się grać, służy
głównie sprawdzeniu dokładności dokumentacji (bo jak inaczej można
udowodnić wierne odtworzenie sprzętu?).

%package tools
Summary:	Additional tools for MAME
Group:		X11/Applications/Games

%description tools
Additional tools for MAME.

%package data
Summary:	Data files used by MAME
Group:		X11/Applications/Games
BuildArch:	noarch

%description data
Data files used by MAME.

%prep
%setup -q -n %{name}-%{name}%{fver}
%patch -P0 -p1

%if %{with system_lua}
%{__sed} -i -e 's/"lua"/"lua5.4"/' scripts/src/main.lua
%endif

%build
%{__make} \
%ifarch %{arm} ppc ppc64 s390 s390x sparc sparcv9 sparc64
	BIGENDIAN=1 \
%endif
%ifarch %{x8664} alpha ia64 ppc64 s390x sparc64
	PTR64=1 \
%endif
%ifarch x32
	PTR64=0 \
	ARCHITECTURE= \
%endif
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LD="%{__cxx}" \
#	OPT_FLAGS="%{rpmcflags}%{?with_system_lua: $(pkg-config --cflags lua5.4)}" \
#	LDFLAGS="%{rpmldflags}%{?with_system_lua: $(pkg-config --libs lua5.4)}" \
	QT_HOME=%{_libdir}/qt6 \
	NOWERROR=1 \
	OSD=sdl \
	TOOLS=1 \
	%{?with_system_lua:USE_SYSTEM_LIB_LUA=1} \
	USE_SYSTEM_LIB_ASIO=1 \
	USE_SYSTEM_LIB_EXPAT=1 \
	USE_SYSTEM_LIB_FLAC=1 \
	USE_SYSTEM_LIB_GLM=1 \
	USE_SYSTEM_LIB_JPEG=1 \
	USE_SYSTEM_LIB_PORTAUDIO=1 \
	USE_SYSTEM_LIB_PORTMIDI=1 \
	USE_SYSTEM_LIB_PUGIXML=1 \
	USE_SYSTEM_LIB_RAPIDJSON=1 \
	USE_SYSTEM_LIB_SQLITE3=1 \
	USE_SYSTEM_LIB_UTF8PROC=1 \
	USE_SYSTEM_LIB_ZLIB=1 \
	USE_SYSTEM_LIB_ZSTD=1 \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_bindir},%{_mandir}/man{1,6}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{cheats,chds,crosshair,ctrlr,effects,fonts,roms,samples,shader}

cat > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.ini << EOF
# Define multi-user paths
artpath            %{_datadir}/%{name}/artwork;%{_datadir}/%{name}/effects
bgfx_path          %{_datadir}/%{name}/bgfx
cheatpath          %{_datadir}/%{name}/cheats
crosshairpath      %{_datadir}/%{name}/crosshair
ctrlrpath          %{_datadir}/%{name}/ctrlr
fontpath           %{_datadir}/%{name}/fonts
hashpath           %{_datadir}/%{name}/hash
languagepath       %{_datadir}/%{name}/language
pluginspath        %{_datadir}/%{name}/plugins
rompath            %{_datadir}/%{name}/roms;%{_datadir}/%{name}/chds;\$HOME/.local/share/%{name}/roms
samplepath         %{_datadir}/%{name}/samples

# Allow user to override ini settings
inipath            \$HOME/.config/%{name};\$HOME/.%{name}/ini;%{_sysconfdir}/%{name}

# Set paths for local storage
cfg_directory      \$HOME/.config/%{name}/cfg;\$HOME/.%{name}/cfg
comment_directory  \$HOME/.config/%{name}/comments;\$HOME/.%{name}/comments
diff_directory     \$HOME/.config/%{name}/diff;\$HOME/.%{name}/diff
input_directory    \$HOME/.config/%{name}/inp;\$HOME/.%{name}/inp
nvram_directory    \$HOME/.local/state/%{name}/nvram;\$HOME/.%{name}/nvram
snapshot_directory \$HOME/.local/state/%{name}/snap;\$HOME/.%{name}/snap
state_directory    \$HOME/.local/state/%{name}/sta;\$HOME/.%{name}/sta
EOF

cp -p %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

cp -p castool chdman floptool imgtool jedutil ldresample ldverify \
    nltool nlwav pngcmp regrep romcmp srcclean unidasm $RPM_BUILD_ROOT%{_bindir}
cp -p split $RPM_BUILD_ROOT%{_bindir}/%{name}-split

cp -a artwork bgfx hash keymaps plugins $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p src/osd/modules/opengl/shader/*.?sh $RPM_BUILD_ROOT%{_datadir}/%{name}/shader

cp -p docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p docs/man/*.6 $RPM_BUILD_ROOT%{_mandir}/man6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%attr(755,root,root) %{_bindir}/mame
%dir %{_sysconfdir}/%{name}
%{_mandir}/man6/mame.6*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/castool
%attr(755,root,root) %{_bindir}/chdman
%attr(755,root,root) %{_bindir}/floptool
%attr(755,root,root) %{_bindir}/imgtool
%attr(755,root,root) %{_bindir}/jedutil
%attr(755,root,root) %{_bindir}/ldresample
%attr(755,root,root) %{_bindir}/ldverify
%attr(755,root,root) %{_bindir}/nltool
%attr(755,root,root) %{_bindir}/nlwav
%attr(755,root,root) %{_bindir}/pngcmp
%attr(755,root,root) %{_bindir}/regrep
%attr(755,root,root) %{_bindir}/romcmp
%attr(755,root,root) %{_bindir}/%{name}-split
%attr(755,root,root) %{_bindir}/srcclean
%attr(755,root,root) %{_bindir}/unidasm
%{_mandir}/man1/castool.1*
%{_mandir}/man1/chdman.1*
%{_mandir}/man1/floptool.1*
%{_mandir}/man1/imgtool.1*
%{_mandir}/man1/jedutil.1*
%{_mandir}/man1/ldplayer.1*
%{_mandir}/man1/ldresample.1*
%{_mandir}/man1/ldverify.1*
%{_mandir}/man1/romcmp.1*

%files data
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/artwork
%{_datadir}/%{name}/bgfx
%{_datadir}/%{name}/chds
%{_datadir}/%{name}/cheats
%{_datadir}/%{name}/effects
%{_datadir}/%{name}/fonts
%{_datadir}/%{name}/keymaps
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/roms
%{_datadir}/%{name}/samples
%{_datadir}/%{name}/shader
%{_datadir}/%{name}/hash
