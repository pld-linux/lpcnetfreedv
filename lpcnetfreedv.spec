#
# Conditional build:
%bcond_with	avx	# x86 AVX instructions
%bcond_with	avx2	# x86 AVX2 instructions
%bcond_with	armneon	# ARM NEON instructions

Summary:	LPCNet for FreeDV
Summary(pl.UTF-8):	LPCNet dla FreeDV
Name:		lpcnetfreedv
Version:	0.3
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/drowe67/LPCNet/releases
Source0:	https://github.com/drowe67/LPCNet/archive/v%{version}/LPCNet-%{version}.tar.gz
# Source0-md5:	81b850852bddfd92c264ba5f9c05d089
Source1:	http://rowetel.com/downloads/deep/lpcnet_191005_v1.0.tgz
# Source1-md5:	a86894b209a1869b50454fe591f047a1
URL:		https://github.com/drowe67/LPCNet
BuildRequires:	cmake >= 3.0
BuildRequires:	codec2-devel >= 0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Experimental version of LPCNet that has been used to develop FreeDV
2020 - a HF radio Digital Voice mode for over the air experimentation
with Neural Net speech coding. Possibly the first use of Neural Net
speech coding in real world operation.

%description -l pl.UTF-8
Eksperymentalna wersja LPCNet, używana przy tworzeniu FreeDV 2020 - 
trybu radiowego dźwięku cyfrowego do eksperymentowania z kodowaniem
mowy opartym na sieci neuronowej. Jest to prawdopodobnie pierwsze
zastosowanie praktyczne kodowania mowy z użyciem sieci neuronowej.

%package devel
Summary:	Development files for LPCNet
Summary(pl.UTF-8):	Pliki programistyczne LPCNet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for LPCNet.

%description devel -l pl.UTF-8
Pliki programistyczne LPCNet.

%prep
%setup -q -n LPCNet-%{version}

%build
install -d build
cd build
# Add model data archive to the build directory so CMake finds it.
cp %{SOURCE1} .

%cmake .. \
	-DDISABLE_CPU_OPTIMIZATION=ON \
	%{?with_avx:-DAVX=ON} \
	%{?with_avx2:-DAVX2=ON} \
	%{?with_armneon:-DNEON=ON}

%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/lpcnet_dec
%attr(755,root,root) %{_bindir}/lpcnet_enc
%attr(755,root,root) %{_libdir}/liblpcnetfreedv.so.0.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblpcnetfreedv.so
%{_includedir}/lpcnet
%{_libdir}/cmake/lpcnetfreedv
