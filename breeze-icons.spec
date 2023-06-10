%define stable %([ "$(echo %{version} |cut -d. -f3)" -ge 70 ] && echo -n un; echo -n stable)

Summary:	Breeze icon theme
Name:		breeze-icons
Version:	5.107.0
Release:	1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
Source0:	http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5IconThemes)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	libxml2-utils
BuildRequires:	python-lxml
BuildRequires:	util-linux-core
BuildArch:	noarch
Requires:	hicolor-icon-theme

%description
Breeze icon theme. Compliant with FreeDesktop.org naming schema.

%files
%dir %{_iconsdir}/breeze
%dir %{_iconsdir}/breeze-dark
%{_iconsdir}/breeze*/actions
%{_iconsdir}/breeze*/animations
%{_iconsdir}/breeze*/applets
%{_iconsdir}/breeze*/apps
%{_iconsdir}/breeze*/categories
%{_iconsdir}/breeze*/devices
%{_iconsdir}/breeze*/emblems
%{_iconsdir}/breeze*/emotes
%{_iconsdir}/breeze*/mimetypes
%{_iconsdir}/breeze*/places
%{_iconsdir}/breeze*/preferences
%{_iconsdir}/breeze*/status
%{_iconsdir}/breeze*/index.theme
%{_iconsdir}/breeze*/*.rcc
%ghost %{_iconsdir}/breeze/icon-theme.cache
%ghost %{_iconsdir}/breeze-dark/icon-theme.cache

#-----------------------------------------------------------------------------

%prep
%autosetup -p1
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

# (crazy) fix calamares not showing right icons here
# reason is we use static names in /home for live user
# that working fine for EN , but now we boot != EN
# and the $HOME/ dirs are translated to whatever language.
# in this case DE is using generic names and pulls $basename.svg
# from theme , which are then the icons from here :)
# We do not needed these , we provide own calamares icon so wipe away.

rm -rf %{buildroot}%{_iconsdir}/breeze/apps/48/calamares.svg
rm -rf %{buildroot}%{_iconsdir}/breeze-dark/apps/48/calamares.svg

# (tpg) try reduce size
hardlink -c -v %{buildroot}%{_iconsdir}

touch  %{buildroot}%{_iconsdir}/{breeze,breeze-dark}/icon-theme.cache

# automatic gtk icon cache update on rpm installs/removals
%transfiletriggerin -- %{_iconsdir}/breeze
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze &>/dev/null || :
fi

%transfiletriggerin -- %{_iconsdir}/breeze-dark
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze-dark &>/dev/null || :
fi

%transfiletriggerpostun -- %{_iconsdir}/breeze
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze &>/dev/null || :
fi

%transfiletriggerpostun -- %{_iconsdir}/breeze-dark
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze-dark &>/dev/null || :
fi
