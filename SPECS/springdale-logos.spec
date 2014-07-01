%global codename verne
%global dist .sdl7

Name: springdale-logos
Summary: Springdale-related icons and pictures
Version: 70.0.5 
Release: 2%{?dist}
Group: System Environment/Base
URL: http://springdale.princeton.edu
# No upstream, done in internal git
Source0: springdale-logos-%{version}.tar.xz
License: GPLv2
BuildArch: noarch
Obsoletes: gnome-logos
Obsoletes: fedora-logos <= 16.0.2-2
Obsoletes: redhat-logos
Provides: gnome-logos = %{version}-%{release}
Provides: system-logos = %{version}-%{release}
Provides: redhat-logos = %{version}-%{release}
# We carry the GSettings schema override, tell that to gnome-desktop3
Provides: system-backgrounds-gnome
Conflicts: kdebase <= 3.1.5
Conflicts: anaconda-images <= 10
Conflicts: redhat-artwork <= 5.0.5
# For splashtolss.sh
#FIXME: dropped for now since it's not available yet
#BuildRequires: syslinux-perl, netpbm-progs
Requires(post): coreutils
BuildRequires: hardlink
# For _kde4_* macros:
BuildRequires: kde-filesystem

%description
The springdale-logos package (the "Package") contains files created by
Springdale Linux to replace the Red Hat "Shadow Man" logo and  RPM logo.
The Red Hat "Shadow Man" logo, RPM, and the RPM logo are trademarks or
registered trademarks of Red Hat, Inc.

%prep
%setup -q

%build

%install
# should be ifarch i386
mkdir -p $RPM_BUILD_ROOT/boot/grub
install -p -m 644 -D bootloader/splash.xpm.gz $RPM_BUILD_ROOT/boot/grub/splash.xpm.gz
# end i386 bits

mkdir -p $RPM_BUILD_ROOT%{_datadir}/backgrounds/
for i in backgrounds/*.jpg backgrounds/*.png backgrounds/default.xml; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/backgrounds/
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
install -p -m 644 backgrounds/10_org.gnome.desktop.background.default.gschema.override $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/
install -p -m 644 backgrounds/desktop-backgrounds-default.xml $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/firstboot/themes/fedora-%{codename}/
for i in firstboot/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/firstboot/themes/fedora-%{codename}/
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/pixmaps
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
for i in plymouth/charge/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
done

for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  for i in icons/hicolor/$size/apps/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/icon-panel-menu.png
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/gnome-main-menu.png
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/kmenu.png
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/start-here.png
  done
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
pushd $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_datadir}/icons/hicolor/16x16/apps/fedora-logo-icon.png favicon.png
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/xfce4_xicon1.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/fedora-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg

(cd anaconda; make DESTDIR=$RPM_BUILD_ROOT install)

for i in 16 22 24 32 36 48 96 256 ; do
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/${i}x${i}/places/start-here-kde-fedora.png 
done

# ksplash theme
mkdir -p $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/
cp -rp kde-splash/Springdale7/ $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/
pushd $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/Springdale7/2560x1600/
ln -s %{_datadir}/backgrounds/day.jpg background.jpg
ln -s %{_datadir}/pixmaps/system-logo-white.png logo.png
popd

# kdm theme
mkdir -p $RPM_BUILD_ROOT/%{_kde4_appsdir}/kdm/themes/
cp -rp kde-kdm/Springdale7/ $RPM_BUILD_ROOT/%{_kde4_appsdir}/kdm/themes/
pushd $RPM_BUILD_ROOT/%{_kde4_appsdir}/kdm/themes/Springdale7/
ln -s %{_datadir}/pixmaps/system-logo-white.png system-logo-white.png
popd

# kde wallpaper theme
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/wallpapers/
cp -rp kde-plasma/Springdale7/ $RPM_BUILD_ROOT/%{_datadir}/wallpapers
pushd $RPM_BUILD_ROOT/%{_datadir}/wallpapers/Springdale7/contents/images
ln -s %{_datadir}/backgrounds/day.jpg 2560x1600.jpg
popd

pushd $RPM_BUILD_ROOT/%{_datadir}/wallpapers/
ln -s %{_datadir}/backgrounds .
popd

# kde desktop theme
mkdir -p $RPM_BUILD_ROOT/%{_kde4_appsdir}/desktoptheme/
cp -rp kde-desktoptheme/* $RPM_BUILD_ROOT/%{_kde4_appsdir}/desktoptheme/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a springdale/*.svg $RPM_BUILD_ROOT%{_datadir}/%{name}

# save some dup'd icons
/usr/sbin/hardlink -v %{buildroot}/

%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/icons/Bluecurve || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor || :
  touch --no-create %{_datadir}/icons/Bluecurve || :
  touch --no-create %{_kde4_iconsdir}/oxygen ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%doc COPYING CREDITS
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/backgrounds/*
%{_datadir}/glib-2.0/schemas/*.override
%{_datadir}/gnome-background-properties/*
%{_datadir}/firstboot/themes/fedora-%{codename}/
%{_datadir}/plymouth/themes/charge/
%{_kde4_iconsdir}/oxygen/
%{_kde4_appsdir}/ksplash/Themes/Springdale7/
%{_kde4_appsdir}/kdm/themes/Springdale7/
%{_kde4_datadir}/wallpapers/Springdale7/
%{_kde4_appsdir}/desktoptheme/Springdale7/

%{_datadir}/pixmaps/*
%{_datadir}/anaconda/boot/splash.lss
%{_datadir}/anaconda/boot/syslinux-splash.png
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/Bluecurve/*/apps/*
%{_datadir}/%{name}/
%{_datadir}/wallpapers/backgrounds

# we multi-own these directories, so as not to require the packages that
# provide them, thereby dragging in excess dependencies.
%dir %{_datadir}/icons/Bluecurve/
%dir %{_datadir}/icons/Bluecurve/16x16/
%dir %{_datadir}/icons/Bluecurve/16x16/apps/
%dir %{_datadir}/icons/Bluecurve/22x22/
%dir %{_datadir}/icons/Bluecurve/22x22/apps/
%dir %{_datadir}/icons/Bluecurve/24x24/
%dir %{_datadir}/icons/Bluecurve/24x24/apps/
%dir %{_datadir}/icons/Bluecurve/32x32/
%dir %{_datadir}/icons/Bluecurve/32x32/apps/
%dir %{_datadir}/icons/Bluecurve/36x36/
%dir %{_datadir}/icons/Bluecurve/36x36/apps/
%dir %{_datadir}/icons/Bluecurve/48x48/
%dir %{_datadir}/icons/Bluecurve/48x48/apps/
%dir %{_datadir}/icons/Bluecurve/96x96/
%dir %{_datadir}/icons/Bluecurve/96x96/apps/
%dir %{_datadir}/icons/Bluecurve/256x256/
%dir %{_datadir}/icons/Bluecurve/256x256/apps/
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/16x16/
%dir %{_datadir}/icons/hicolor/16x16/apps/
%dir %{_datadir}/icons/hicolor/22x22/
%dir %{_datadir}/icons/hicolor/22x22/apps/
%dir %{_datadir}/icons/hicolor/24x24/
%dir %{_datadir}/icons/hicolor/24x24/apps/
%dir %{_datadir}/icons/hicolor/32x32/
%dir %{_datadir}/icons/hicolor/32x32/apps/
%dir %{_datadir}/icons/hicolor/36x36/
%dir %{_datadir}/icons/hicolor/36x36/apps/
%dir %{_datadir}/icons/hicolor/48x48/
%dir %{_datadir}/icons/hicolor/48x48/apps/
%dir %{_datadir}/icons/hicolor/96x96/
%dir %{_datadir}/icons/hicolor/96x96/apps/
%dir %{_datadir}/icons/hicolor/256x256/
%dir %{_datadir}/icons/hicolor/256x256/apps/
%dir %{_datadir}/icons/hicolor/scalable/
%dir %{_datadir}/icons/hicolor/scalable/apps/
%dir %{_datadir}/anaconda
%dir %{_datadir}/anaconda/pixmaps
%dir %{_datadir}/anaconda/boot/
%dir %{_datadir}/firstboot/
%dir %{_datadir}/firstboot/themes/
%dir %{_datadir}/plymouth/
%dir %{_datadir}/plymouth/themes/
%dir %{_kde4_sharedir}/kde4/
%dir %{_kde4_appsdir}
%dir %{_kde4_appsdir}/ksplash
%dir %{_kde4_appsdir}/ksplash/Themes/
# should be ifarch i386
/boot/grub/splash.xpm.gz
# end i386 bits

%changelog
* Tue Jun 24 2014 Thomas Uphill <thomas@narrabilis.com> - 70.0.5-2
- Initial Build, based on centos-logos, see centos-logos for full changelog
