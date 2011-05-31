use strict;
use warnings;

use ExtUtils::MakeMaker 6.31;

my %PREREQ_PM = map { my ( $package, $version ) = split m/\s/; ( $package => $version || 0 ) } grep { m/\S/ } grep { ! /^\s*#/ } split m/\n/, <<_END_;
Test::Most
Test::HTTP
_END_

my %WriteMakefileArgs = (
  'ABSTRACT' => '',
  'AUTHOR' => '',
  'BUILD_REQUIRES' => {
  },
  'CONFIGURE_REQUIRES' => {
    'ExtUtils::MakeMaker' => '6.31'
  },
  'DISTNAME' => 'Task-t-gist-it',
  'EXE_FILES' => [],
  'LICENSE' => 'perl',
  'NAME' => 'Task::BuildRule90',
  'PREREQ_PM' => { %PREREQ_PM },
  'VERSION' => '0.001',
  'test' => {
    'TESTS' => 't/*.t'
  }
);


unless ( eval { ExtUtils::MakeMaker->VERSION(6.56) } ) {
  my $br = delete $WriteMakefileArgs{BUILD_REQUIRES};
  my $pp = $WriteMakefileArgs{PREREQ_PM};
  for my $mod ( keys %$br ) {
    if ( exists $pp->{$mod} ) {
      $pp->{$mod} = $br->{$mod} if $br->{$mod} > $pp->{$mod};
    }
    else {
      $pp->{$mod} = $br->{$mod};
    }
  }
}

delete $WriteMakefileArgs{CONFIGURE_REQUIRES}
  unless eval { ExtUtils::MakeMaker->VERSION(6.52) };

WriteMakefile(%WriteMakefileArgs);

