Summary:	Mesa Demos source code
Summary(pl.UTF-8):	Kod źródłowy programów demonstrujących dla bibliotek Mesa
Name:		mesa-demos
Version:	8.1.0
Release:	1
License:	various (MIT, SGI, GPL - see copyright notes in sources)
Group:		Development/Libraries
Source0:	ftp://ftp.freedesktop.org/pub/mesa/demos/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	9df33ba69a26bbfbc7c8148602e59542
URL:		http://www.mesa3d.org/
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	glew-devel >= 1.5.4
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
Requires:	OpenGL-devel
Requires:	OpenGL-glut-devel
Obsoletes:	Mesa-demos
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Demonstration programs for the Mesa libraries in source code form.

%description -l pl.UTF-8
Kod źródłowy programów demonstracyjnych dla bibliotek Mesa.

%package -n mesa-utils
Summary:	OpenGL utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe OpenGL z projektu Mesa3D
License:	MIT
Group:		X11/Applications/Graphics
Obsoletes:	Mesa-utils
# loose deps on libGL/libGLU

%description -n mesa-utils
OpenGL utilities from Mesa3D: glxgears and glxinfo.

%description -n mesa-utils -l pl.UTF-8
Programy narzędziowe OpenGL z projektu Mesa3D: glxgears i glxinfo.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules

# we only want glxinfo and glxgears to be built here
%{__make} -C src/xdemos

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_examplesdir}/%{name}-%{version}}

install -p src/xdemos/{glxinfo,glxgears} $RPM_BUILD_ROOT%{_bindir}

cp -a * $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__make} -C $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} distclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files -n mesa-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/glxgears
%attr(755,root,root) %{_bindir}/glxinfo
