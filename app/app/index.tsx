// Root entry — decides whether the user goes through onboarding or straight home.
import { Redirect } from 'expo-router';
import { useProfile } from '@/store/profile';

export default function Index() {
  const profile = useProfile((s) => s.profile);
  return profile ? <Redirect href="/(tabs)/home" /> : <Redirect href="/onboarding/welcome" />;
}
