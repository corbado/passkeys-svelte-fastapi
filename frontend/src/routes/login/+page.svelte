<script lang="ts">
	import Corbado from '@corbado/web-js';
	import userStore from '../../stores/user.svelte';
	import { goto } from '$app/navigation';

	$effect(() => {
		switch (userStore.externalUserInfo.status) {
			case 'success':
				if (userStore.externalUserInfo.user.city === null) {
					goto('/signup/onboarding');
				} else {
					goto('/profile');
				}
				return;
			case 'error':
				// handle this case more gracefully in a real application
				console.error(userStore.externalUserInfo.message);
				return;
		}
	});

	let loginDiv: HTMLDivElement;

	userStore.onCorbadoLoaded(() => {
		Corbado.mountAuthUI(loginDiv, {
			initialBlock: 'login-init',
			onLoggedIn() {
				// do nothing here. We have to wait for a backend response
				// to check whether the user has gone through onboarding already.
				// The backend call is made in the user store.
			}
		});
	});
</script>

<h1>Login</h1>
<div bind:this={loginDiv}></div>
