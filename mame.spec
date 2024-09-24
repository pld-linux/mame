# TODO: is qt optional? (either as bcond, or qt-less version)
%define		fver	%(echo %{version} | tr -d .)
Summary:	MAME - Multiple Arcade Machine Emulator
Summary(pl.UTF-8):	MAME (Multiple Arcade Machine Emulator) - emulator wielu automatów do gier
Name:		mame
Version:	0.249
Release:	1
License:	GPL v2+ (BSD for core part, LGPL v2.1+/GPL v2+ for some drivers)
Group:		X11/Applications/Games
#Source0Download: https://www.mamedev.org/release.html
Source0:	https://github.com/mamedev/mame/archive/mame%{fver}/%{name}-%{version}.tar.gz
# Source0-md5:	37b527a7b769b0d7d000ab512a5151ac
URL:		https://www.mamedev.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	SDL2-devel >= 2
BuildRequires:	SDL2_ttf-devel >= 2
BuildRequires:	alsa-lib-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flac-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	libjpeg-devel
BuildRequires:	lua53-devel >= 5.3
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	portmidi-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	unzip
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	zlib-devel
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

%prep
%setup -q -n %{name}-%{name}%{fver}

%{__sed} -i -e 's/"lua"/"lua5.3"/' scripts/src/main.lua

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
	OPT_FLAGS="%{rpmcflags} $(pkg-config --cflags lua5.3)" \
	LDFLAGS="%{rpmldflags}" \
	CPP11=1 \
	NOWERROR=1 \
	OSD=sdl \
	USE_SYSTEM_LIB_EXPAT=1 \
	USE_SYSTEM_LIB_FLAC=1 \
	USE_SYSTEM_LIB_JPEG=1 \
	USE_SYSTEM_LIB_LUA=1 \
	USE_SYSTEM_LIB_PORTAUDIO=1 \
	USE_SYSTEM_LIB_PORTMIDI=1 \
	USE_SYSTEM_LIB_SQLITE3=1 \
	USE_SYSTEM_LIB_ZLIB=1 \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install mame $RPM_BUILD_ROOT%{_bindir}/mame

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/mame
