Name:		sauerbraten
Version:	2013_02_03
Release:	1
Summary:	A multi-player/single-player first person shooter
Group:		Games/Arcade
License:	ZLIB license, BSD
URL:		http://www.sauerbraten.org/
Source0:	http://switch.dl.sourceforge.net/project/sauerbraten/sauerbraten/%{version}/sauerbraten_%{version}_collect_edition_linux.tar.bz2
Source1:	%{name}.png
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libenet) >= 1.3.5
Requires:	%{name}-data = %{EVRD}

%description
Free multi-player/single-player first person shooter, built as a major
redesign of the Cube FPS.

Much like the original Cube, the aim of this game is not necessarily
to produce the most features & eye-candy possible, but rather to
allow map/geometry editing to be done dynamically in-game, to create
fun game-play and an elegant engine.

The engine supporting the game is entirely original in code & design,
and its code is Open Source (ZLIB license, read the docs for more on
how you can use the engine).

In addition to the FPS game which is in a very playable state, the
engine is being used for an RPG which is in the preproduction phase.
Additionally, Proper Games ltd are the first to use the engine
commercially. dot3 labs is a company started by the creators of
sauerbraten that offers commercial support.

%files
%doc docs/*
%{_bindir}/%{name}.sh
%{_gamesbindir}/sauer_client
%{_datadir}/pixmaps/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop

#-----------------------------------------------------------------------------

%package server
Summary:	Standalone Sauerbraten server for LAN and Internet gaming
Group:		Games/Arcade
Requires:	%{name}-data = %{EVRD}

%description server
Sauerbraten (a.k.a. Cube 2) is a free multi-player/single-player
first person shooter, built as a major redesign of the Cube FPS.
This package is useful if you only need the Sauerbraten server and
not the game itself.

This package contains a standalone server.

%files server
%{_bindir}/%{name}-server.sh
%{_gamesbindir}/sauer_server

#-----------------------------------------------------------------------------

%package data
Summary:	Standalone Sauerbraten server for LAN and Internet gaming
Group:		Games/Arcade
Conflicts:	%{name} < 2013_02_03
BuildArch:	noarch

%description data
Sauerbraten (a.k.a. Cube 2) is a free multi-player/single-player
first person shooter, built as a major redesign of the Cube FPS.
This package is useful if you only need the Sauerbraten server and
not the game itself.

%files data
%{_gamesdatadir}/%{name}

#-----------------------------------------------------------------------------

%prep
%setup -q -n %{name}
rm -rf bin_unix/*

%build
# flags for enet
%setup_compile_flags
pushd src
	%make
popd

%install
# engine --------------------------------------------------------------------
mkdir -p %{buildroot}%{_gamesbindir}
install -m 755 src/sauer_client %{buildroot}%{_gamesbindir}
install -m 755 src/sauer_server %{buildroot}%{_gamesbindir}

# startscripts --------------------------------------------------------------
cat > %{name}.sh <<EOF
#!/bin/bash
CUBE_DIR=\$HOME/.%{name}
if [ ! -d \$CUBE_DIR ]; then
	mkdir -p \$CUBE_DIR
	cd \$CUBE_DIR
	ln -s %{_gamesbindir}/sauer_*  .
	ln -s %{_gamesdatadir}/%{name}/* .
	rm server*.cfg 2> /dev/null
fi

cd \$CUBE_DIR
ln -sf %{_gamesbindir}/sauer_*  .
ln -sf %{_gamesdatadir}/%{name}/* .
exec ./sauer_client \$*
EOF

cat > %{name}-server.sh <<EOF
#!/bin/bash
CUBE_DIR=\$HOME/.%{name}
if [ ! -d \$CUBE_DIR ]; then
	mkdir -p \$CUBE_DIR
	cd \$CUBE_DIR
	ln -s %{_gamesbindir}/sauer_* .
	ln -s %{_gamesdatadir}/%{name}/* .
	rm server*.cfg 2> /dev/null
	cp %{_gamesdatadir}/%{name}/server*.cfg .
fi
# server.cfg ==> servers.cfg
if [ ! -e \$CUBE_DIR/servers.cfg ]; then
	cd \$CUBE_DIR
	rm servers.cfg 2> /dev/null
	cp %{_gamesdatadir}/%{name}/servers.cfg .
fi
# new in troopers server-init.cfg
if [ ! -e \$CUBE_DIR/server-init.cfg ]; then
	cd \$CUBE_DIR
	rm server-init.cfg 2> /dev/null
	cp %{_gamesdatadir}/%{name}/server-init.cfg .
fi
cd \$CUBE_DIR
exec ./sauer_server \$*
EOF

mkdir -p %{buildroot}%{_bindir}
install -m 755 %{name}*.sh %{buildroot}%{_bindir}

# install the menu icon -----------------------------------------------------
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps

# need for simple-welcome ---------------------------------------------------
mkdir -p %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -size 16x16 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
convert -size 32x32 %{SOURCE1} %{buildroot}%{_iconsdir}/%{name}.png
convert -size 48x48 %{SOURCE1} %{buildroot}%{_liconsdir}/%{name}.png

# menu entry ----------------------------------------------------------------
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Sauerbraten
Comment=A multi-player/single-player first person shooter
Comment[ru]=Sauerbraten - одно/многопользовательский шутер от первого лица
Exec=%{_bindir}/%{name}.sh
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;ArcadeGame;
EOF

# data files ----------------------------------------------------------------
mkdir -p %{buildroot}%{_gamesdatadir}/%{name}
cp -a data packages %{buildroot}%{_gamesdatadir}/%{name}

