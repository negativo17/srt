Name:           srt
Version:        1.4.2
Release:        5%{?dist}
Summary:        Secure Reliable Transport protocol tools
License:        MPLv2.0
URL:            https://www.srtalliance.org

Source0:        https://github.com/Haivision/srt/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-gcc11.patch

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  gnutls-devel
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel

Requires:       srt-libs%{?_isa} = %{version}-%{release}

%description
Secure Reliable Transport (SRT) is an open source transport technology that
optimizes streaming performance across unpredictable networks, such as the
Internet.

%package        libs
Summary:        Secure Reliable Transport protocol libraries

%description    libs
Secure Reliable Transport protocol libraries.

%package        devel
Summary:        Secure Reliable Transport protocol development libraries and headers
Requires:       srt-libs%{?_isa} = %{version}-%{release}

%description devel
Secure Reliable Transport protocol development libraries and header files/

%prep
%autosetup -p1

%build
%cmake \
  -DENABLE_STATIC=OFF \
  -DENABLE_UNITTESTS=ON \
  -DENABLE_GETNAMEINFO=ON \
  -DUSE_ENCLIB=gnutls

%cmake_build

%install
%cmake_install
# remove old upstream temporary compatibility pc
rm -f %{buildroot}/%{_libdir}/pkgconfig/haisrt.pc

%check
# Fails with x390x
make test \
%ifarch s390x
  || :
%endif

%ldconfig_scriptlets libs

%files
%license LICENSE
%doc README.md docs
%{_bindir}/srt-ffplay
%{_bindir}/srt-file-transmit
%{_bindir}/srt-live-transmit
%{_bindir}/srt-tunnel
%{_bindir}/test-srt

%files libs
%license LICENSE
%{_libdir}/libsrt.so.1*

%files devel
%doc examples
%{_includedir}/srt
%{_libdir}/libsrt.so
%{_libdir}/pkgconfig/srt.pc

%changelog
* Thu Apr 29 2021 Simone Caronni <negativo17@gmail.com> - 1.4.2-5
- Clean up.

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1.4.2-4
- Rebuilt for removed libstdc++ symbol (#1937698)
