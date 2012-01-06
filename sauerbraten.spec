%define use_ccache	1
%define ccachedir	~/.ccache-OOo%{mdvsuffix}
%{?_with_ccache: %global use_ccache 1}
%{?_without_ccache: %global use_ccache 0}
%define name	sauerbraten
%define version 2010_07_28
%define release %mkrel 2
%define _enable_debug_packages	%{nil}
%define debug_package %{nil}
%define _prefix	/usr

Name:		%{name}
Version:        %{version}
Release:        %{release}
Summary:	Sauerbraten - A multiplayer/singleplayer first person shooter
License:	ZLIB license, BSD
URL:		http://www.sauerbraten.org/
Group:		Games/Arcade
Source0:	sauerbraten_%{version}_justice_edition_linux.tar.bz2
Source1:	%{name}.png
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	gcc-c++
BuildRequires:	libpng-devel
BuildRequires:	mesa-common-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel 
BuildRequires:	unzip
BuildRequires:	desktop-file-utils
BuildRequires:	zlib1-devel
BuildRequires:	enet-devel
Requires:	enet

%description
Sauerbraten (a.k.a. Cube 2) is a free multiplayer/singleplayer
first person shooter, built as a major redesign of the Cube FPS.

Much like the original Cube, the aim of this game is not necessarily
to produce the most features & eyecandy possible, but rather to
allow map/geometry editing to be done dynamically in-game, to create
fun gameplay and an elegant engine.

The engine supporting the game is entirely original in code & design,
and its code is Open Source (ZLIB license, read the docs for more on
how you can use the engine).

In addition to the FPS game which is in a very playable state, the
engine is being used for an RPG which is in the preproduction phase.
Additionally, Proper Games ltd are the first to use the engine
commercially. dot3 labs is a company started by the creators of
sauerbraten that offers commercial support.

%package server
Summary:	Standalone Sauerbraten server for LAN and Internet gaming
Group:		Games/Arcade

%description server
Sauerbraten (a.k.a. Cube 2) is a free multiplayer/singleplayer
first person shooter, built as a major redesign of the Cube FPS.
This package is useful if you only need the Sauerbraten server and not the game itself.
This package contains a standalone server.


%prep
%setup -q -n %{name}

%__install -dm 755 bin_unix

%build
# flags for enet
export CFLAGS="$RPM_OPT_FLAGS"
export CPPFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
pushd src
	%__make %{?jobs:-j%{jobs}} \
		CXXFLAGS="$RPM_OPT_FLAGS"
popd

%install
%__rm -fr %{buildroot}

# engine
%__install -dm 755 %{buildroot}%{_prefix}/games/%{name}
%__install -m 755 src/sauer_client %{buildroot}%{_prefix}/games
%__install -m 755 src/sauer_server %{buildroot}%{_prefix}/games

# startscripts
%__cat > %{name}.sh <<EOF
#!/bin/bash
CUBE_DIR=\$HOME/.%{name}
if [ ! -d \$CUBE_DIR ]; then
	mkdir -p \$CUBE_DIR
	cd \$CUBE_DIR
	ln -s %{_prefix}/games/sauer_*  .
	ln -s %{_datadir}/games/%{name}/* .
	rm server*.cfg 2> /dev/null
fi

cd \$CUBE_DIR
ln -sf %{_prefix}/games/sauer_*  .
ln -sf %{_datadir}/games/%{name}/* .
exec ./sauer_client \$*
EOF

%__cat > %{name}-server.sh <<EOF
#!/bin/bash
CUBE_DIR=\$HOME/.%{name}
if [ ! -d \$CUBE_DIR ]; then
	mkdir -p \$CUBE_DIR
	cd \$CUBE_DIR
	ln -s %{_prefix}/games/sauer_* .
	ln -s %{datadir}/games/%{name}/* .
	rm server*.cfg 2> /dev/null
	cp %{_datadir}/games/%{name}/server*.cfg .
fi
# server.cfg ==> servers.cfg
if [ ! -e \$CUBE_DIR/servers.cfg ]; then
	cd \$CUBE_DIR
	rm servers.cfg 2> /dev/null
	cp %{_datadir}/games/%{name}/servers.cfg .
fi
# new in troopers server-init.cfg
if [ ! -e \$CUBE_DIR/server-init.cfg ]; then
	cd \$CUBE_DIR
	rm server-init.cfg 2> /dev/null
	cp %{_datadir}/games/%{name}/server-init.cfg .
fi
cd \$CUBE_DIR
exec ./sauer_server \$*
EOF

%__install -dm 755 %{buildroot}%{_bindir}
%__install -m 755 %{name}*.sh %{buildroot}%{_bindir}

# install the menu icon
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
%__install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps

mkdir $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Sauerbraten
Comment=%{summary}
Comment[ru]=Sauerbraten - одно/многопользовательский шутер от первого лица
Exec=%{_bindir}/%{name}.sh
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

# Data files
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/games/sauerbraten
find . -type d -name CVS | xargs rm -rf || true
cp -a data packages $RPM_BUILD_ROOT/%{_datadir}/games/sauerbraten


%clean
%__rm -fr %{buildroot}

%if %mdkversion < 200900
%post
%{update_desktop_database}
%{update_menus}
%endif
 
%if %mdkversion < 200900
%postun
%{clean_desktop_database}
%{clean_menus} 
%endif


%files
%defattr(-,root,root)
%doc docs/*
%{_bindir}/%{name}.sh
%{_prefix}/games/sauer_client
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_bindir}/%{name}-server.sh
%{_prefix}/games/sauer_server
%dir %{_datadir}/games/sauerbraten
%{_datadir}/games/sauerbraten/data
%{_datadir}/games/sauerbraten/packages


%files server
%defattr(-,root,root)
%{_bindir}/%{name}-server.sh
%{_prefix}/games/sauer_server
